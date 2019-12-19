#!/usr/bin/env python

import os
import sys
import time
import json
import argparse
import websocket
from tornado import web, ioloop, queues, gen, process
from content_processor import ContentProcessor

class TranslatorWorker():

    def __init__(self, srclang,targetlang,service):
        self.q = queues.Queue()
        # Service definition
        self.service = service
        self.p = None
        self.contentprocessor=ContentProcessor(
            srclang,
            targetlang,
            sourcebpe=self.service.get('sourcebpe'),
            targetbpe=self.service.get('targetbpe'),
            sourcespm=self.service.get('sourcespm'),
            targetspm=self.service.get('targetspm')
        )
        self.ws_url = "ws://{}:{}/translate".format(
            self.service['host'], self.service['port'])
        if self.service['configuration']:
            self.run()

    @gen.coroutine
    def run(self):
        process.Subprocess.initialize()
        self.p = process.Subprocess(['marian-server', '-c',
                                     self.service['configuration'],
                                     '--quiet-translation',
                                     '-p', self.service['port']])
        self.p.set_exit_callback(self.on_exit)
        ret = yield self.p.wait_for_exit()

    def on_exit(self):
        print("Process exited")

    def translate(self, srctxt):
        ws = websocket.create_connection(self.ws_url)
        sentences= self.contentprocessor.preprocess(srctxt)
        translatedSentences=[]
        for sentence in sentences:
            ws.send(sentence)
            translatedSentences.append( ws.recv() )
        ws.close()
        translation=self.contentprocessor.postprocess(translatedSentences)
        return ' '.join(translation)


class ApiHandler(web.RequestHandler):
    def initialize(self, worker_pool):
        self.worker_pool = worker_pool
        self.worker = None
        self.args = {}

    def prepare_args(self):
        if self.request.headers['Content-Type'] == 'application/json':
            self.args = json.loads(self.request.body)

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
        self.source_langs = []
        self.target_langs = []
        for source_lang in config:
            targetLangs = config[source_lang]
            for target_lang in targetLangs:
                self.source_langs.append(source_lang)
                self.target_langs.append(target_lang)
        # Remove duplicates
        self.source_langs = list(set(self.source_langs))
        self.target_langs = list(set(self.target_langs))

    def get(self):
        self.render("index.template.html",
                    title="Opus MT", source_langs=self.source_langs, target_langs=self.target_langs)


def initialize_workers(config):
    worker_pool = {}
    for source_lang in config:
        targetLangs = config[source_lang]
        for target_lang in targetLangs:
            lang_pair = "{}-{}".format(source_lang, target_lang)
            decoder_config = targetLangs[target_lang]
            worker_pool[lang_pair] = TranslatorWorker(source_lang, target_lang,decoder_config)

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
        (r"/api", ApiHandler, dict(worker_pool=worker_pool))
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
