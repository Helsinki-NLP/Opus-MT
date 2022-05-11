#!/usr/bin/env python3
#-*-python-*-
#
#

import signal
import sys
import ssl
import argparse
import codecs
import json
# import socket
from websocket import create_connection
from SimpleWebSocketServer import SimpleWebSocketServer, SimpleSSLWebSocketServer, WebSocket

## language identifer (if source language is not given)
import pycld2 as cld2

parser = argparse.ArgumentParser(description='Simple translation server.')
parser.add_argument('-p','--port', type=int, default=8080,
                   help='socket the server will listen on')
parser.add_argument('-c','--config', type=str, default="opusMT-servers.json",
                   help='MT server configurations')
parser.add_argument('-t','--deftrg','--default-target-language', type=str, default='en',
                    help='default target language')
parser.add_argument('-s','--defsrc','--default-source-language', type=str, default='fi',
                    help='default source language')
parser.add_argument('-m','--max-input-length', type=int, default=1000,
                   help='maximum length of the input string')

## SSL options
parser.add_argument("--ssl", default=0, type=int, action="store", dest="ssl",
                  help="ssl (1: on, 0: off (default))")
parser.add_argument("--cert", default='./cert.pem', type=str, action="store", dest="cert",
                  help="cert (./cert.pem)")
parser.add_argument("--key", default='./key.pem', type=str, action="store", dest="key",
                  help="key (./key.pem)")
parser.add_argument("--ver", default=ssl.PROTOCOL_TLSv1_2, type=int, action="store", dest="ver",
                  help="ssl version")


args = parser.parse_args()


with open(args.config, 'r') as f:
    opusMT_servers = json.load(f)


## create a list of web socket connections
## (TODO: does that scale well?)
ws = dict()
opusMT = dict()

for h in opusMT_servers:
    print("open connection to server " + h)
    ws[h] = create_connection("ws://" + h)
    srclangs = opusMT_servers[h]["source-languages"].split('+')
    trglangs = opusMT_servers[h]["target-languages"].split('+')
    model = 'default'
    if 'model' in opusMT_servers[h]:
        model = opusMT_servers[h]["model"]
    for s in srclangs:
        for t in trglangs:
            key = s+'-'+t+'-'+model
            if (not key in opusMT) or (len(srclangs) == 1 and len(trglangs) == 1):
                print(" - serving " + s + t + '-' + model)
                opusMT[key] = h



class Translate(WebSocket):

    def handleMessage(self):

        # print('received: ' + self.data)
        fromLang = None
        toLang = args.deftrg
        prefix = ''
        modelName = 'default'

        try:
            data = json.loads(self.data)
            srctxt = data['text']
            if 'model' in data:
                modelName = data['model']
            if 'source' in data:
                if data['source'] != 'DL' and data['source'] != 'detect':
                    fromLang = data['source']
            if 'target' in data:
                if data['target']:
                    toLang = data['target']
        except ValueError as error:
            # print("invalid json: %s" % error)
            srctxt = self.data
            # check whether the first token specifies the language pair
            srctxt = self.data
            tokens = srctxt.split()
            langs = tokens.pop(0).split('-')
            if len(langs) == 2:
                toLang = langs[1]
                if langs[0] != 'DL' and langs[0] != 'detect':
                    fromLang = langs[0]
                srctxt = " ".join(tokens)

        srctxt = srctxt.strip().replace("\n",' ')
        if not srctxt:
            self.sendMessage(json.dumps({'result': ""}, sort_keys=True, indent=4))
            return

        if len(srctxt) > args.max_input_length:
            self.sendMessage(json.dumps({'result': 'ERROR: Input too long! Maximum length = {}'.format(args.max_input_length)}, sort_keys=True, indent=4))
            return

        if not fromLang:
            isReliable, textBytesFound, details = cld2.detect(srctxt, bestEffort=True)
            fromLang = details[0][1]
            print("language detected = " + fromLang)
            # if fromLang == toLang and toLang != args.defsrc:
            #     toLang = args.defsrc

        # special case: DL as target means to use the same as input
        if toLang == 'DL' or toLang == 'detect':
            toLang=fromLang

        langpair = fromLang + '-' + toLang
        model =  langpair + '-' + modelName
        if not model in opusMT:
            print('unsupported language pair ' + langpair)
            # self.sendMessage('ERROR: unsupported language pair ' + langpair)
            self.sendMessage(json.dumps({'result': 'ERROR: unsupported language pair ' + langpair}, sort_keys=True, indent=4))
            return

        server = opusMT[model]

        record = {'text': srctxt, 'source': fromLang, 'target': toLang}
        message = json.dumps(record, sort_keys=True, indent=4)
        # print("sending to " + server + ":" + message)
        ws[server].send(message)
        translated = ws[server].recv()
        # ws[server].sendall(bytes(message, "utf-8"))
        # translated = str(ws[server].recv(1024), "utf-8")

        # print(translated, flush=True)
        try:
            result = json.loads(translated)
            result['server'] = server
            result['source'] = fromLang
            result['target'] = toLang
            self.sendMessage(json.dumps(result, sort_keys=True, indent=4))
        except ValueError as error:
            print("invalid json: %s" % error)
            self.sendMessage(json.dumps({'result': 'ERROR: {}'.format(error)}, sort_keys=True, indent=4))

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


if args.ssl == 1:
    print("open ssl connection with version " + str(args.ver))
    server = SimpleSSLWebSocketServer('', args.port, Translate,
                                      args.cert, args.key, version=args.ver)
else:   
    server = SimpleWebSocketServer('', args.port, Translate)
server.serveforever()
