#!/usr/bin/env python

import os
import sys
import time
import json
import argparse
import websocket
from tornado import web, ioloop, queues, gen, process
from content_processor import ContentProcessor

class TranslatorInterface():
    """An interface to a single, possibly multilingual, model."""

    def __init__(self, srclang, targetlang, service, model):
        self.service = service
        self.contentprocessor = ContentProcessor(
            srclang,
            targetlang,
            sourcebpe=self.service.get('sourcebpe'),
            targetbpe=self.service.get('targetbpe'),
            sourcespm=self.service.get('sourcespm'),
            targetspm=self.service.get('targetspm')
        )
        self.worker = model
        # becomes nonempty if there are multiple target languages
        self.preamble = ""

    def translate(self, text):
        sentences = self.contentprocessor.preprocess(text)
        translatedSentences = self.worker.translate(self.preamble + '\n'.join(sentences))
        translation = self.contentprocessor.postprocess(translatedSentences)
        return ' '.join(translation)

    def ready(self):
        return self.worker != None and self.worker.ready()

    def on_exit(self):
        if self.worker != None:
            self.worker.on_exit()

class TranslatorWorker():
    """Provides a running instance of marian-server."""

    def __init__(self, host, port, configuration):
        self.host = host
        self.port = port
        self.configuration = configuration
        self.ws_url = "ws://{}:{}/translate".format(host, port)
        self.run()

    @gen.coroutine
    def run(self):
        process.Subprocess.initialize()
        self.p = process.Subprocess(['marian-server', '-c',
                                     self.configuration,
                                     '-p', self.port,
                                     '--allow-unk',
                                     # enables translation with a mini-batch size of 64, i.e. translating 64 sentences at once, with a beam-size of 6.
                                     '-b', '6',
                                     '--mini-batch', '64',
                                     # use a length-normalization weight of 0.6 (this usually increases BLEU a bit).
                                     '--normalize', '0.6',
                                     '--maxi-batch-sort', 'src',
                                     '--maxi-batch', '100',
                                      ])
        self.p.set_exit_callback(self.on_exit)
        ret = yield self.p.wait_for_exit()

    def on_exit(self):
        print("Process exited")

    def translate(self, sentences):
        ws = websocket.create_connection(self.ws_url)
        ws.send(sentences)
        translatedSentences = ws.recv().split('\n')
        ws.close()
        return translatedSentences

    def ready(self):
        try:
            ws = websocket.create_connection(self.ws_url)
            ws.close()
        except ConnectionError:
            return False
        return True

class ApiHandler(web.RequestHandler):
    def initialize(self, api, config, worker_pool):
        self.worker_pool = worker_pool
        self.config = config
        self.api = api
        self.worker = None
        self.args = {}

    def prepare_args(self):
        if self.request.headers['Content-Type'] == 'application/json':
            self.args = json.loads(self.request.body)

    def get(self):
        if self.api == 'ready':
            if all(map(lambda x: x.ready(), self.worker_pool.values())):
                self.set_status(204)
            else:
                self.set_status(500, "Translation server(s) not responding")
        elif self.api == 'languages':
            languages = {}
            for source_lang in self.config:
                languages[source_lang] = []
                targetLangs = self.config[source_lang]
                for target_lang in targetLangs:
                    languages[source_lang].append(target_lang)

            return self.write(dict(languages=languages))

    def post(self):
        self.prepare_args()
        lang_pair = "{}-{}".format(self.args['from'], self.args['to'])
        if lang_pair not in self.worker_pool:
            self.write(
                dict(error="Language pair {} not suppported".format(lang_pair)))
            return
        self.worker = self.worker_pool[lang_pair]
        translation = self.worker.translate(self.args['source'])
        self.write(dict(translation=translation))


class MainHandler(web.RequestHandler):
    def initialize(self, config):
        self.config = config

    def get(self):
        self.render("index.template.html", title="Opus MT")


def initialize_workers(config):
    worker_pool = {}
    models = {}
    for source_lang in config:
        targetLangs = config[source_lang]
        for target_lang in targetLangs:
            lang_pair = "{}-{}".format(source_lang, target_lang)
            pair_config = targetLangs[target_lang]
            if pair_config['configuration'] not in models:
                models[pair_config['configuration']] = TranslatorWorker(
                    pair_config['host'], pair_config['port'], pair_config['configuration'])
            worker_pool[lang_pair] = TranslatorInterface(
                source_lang, target_lang, pair_config, models[pair_config['configuration']])
            # Multi-target models have to be told which language to translate to
            if len(targetLangs) > 1:
                worker_pool[lang_pair].preamble = ">>{}<< ".format(target_lang)

    return worker_pool


settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "static"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
)


def make_app(args):
    services = {}
    with open(args.config, 'r') as configfile:
        services = json.load(configfile)
    worker_pool = initialize_workers(services)
    handlers = [
        (r"/", MainHandler, dict(config=services)),
        (r"/api/translate", ApiHandler,
         dict(api='translate', config=services, worker_pool=worker_pool)),
        (r"/api/ready", ApiHandler,
         dict(api='ready', config=services, worker_pool=worker_pool)),
        (r"/api/languages", ApiHandler,
         dict(api='languages', config=services, worker_pool=worker_pool))
    ]
    application = web.Application(handlers, debug=False, **settings)
    return application


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Marian MT translation server.')
    parser.add_argument('-p', '--port', type=int, default=8888,
                        help='Port the server will listen on')
    parser.add_argument('-c', '--config', type=str, default="services.json",
                        help='MT server configurations')
    args = parser.parse_args()
    application = make_app(args)
    application.listen(args.port)
    ioloop.IOLoop.current().start()
