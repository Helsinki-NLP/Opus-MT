#!/usr/bin/env python3
#-*-python-*-
#
#

import signal
import sys
import argparse
import codecs
import json
from websocket import create_connection
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket


## pre-processing: 
## - moses-script wrapper classes
## - BPE-based segmentation from subword-nmt
from apply_bpe import BPE
from mosestokenizer import *

## language identifer (if source language is not given)
import pycld2 as cld2

parser = argparse.ArgumentParser(description='Simple translation server.')
parser.add_argument('-p','--port', type=int, default=8080,
                   help='socket the server will listen on')
parser.add_argument('-c','--config', type=str, default="opusMT-servers.json",
                   help='MT server configurations')
parser.add_argument('-d','--deftrg','--default-target-language', type=str, default='en',
                    help='default target language (for multilingual models)')

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
    for s in srclangs:
        for t in trglangs:
            print(" - serving " + s + t)
            opusMT[s+'-'+t] = h


class Translate(WebSocket):

    def handleMessage(self):

        # print('received: ' + self.data)
        fromLang = None
        toLang = args.deftrg
        prefix = ''

        ## check whether the first token specifies the language pair
        srctxt = self.data
        tokens = srctxt.split()
        langs = tokens.pop(0).split('-')
        if len(langs) == 2:
            toLang = langs[1]
            if langs[0] != 'DL':
                fromLang = langs[0]
            srctxt = " ".join(tokens)

        if not fromLang:
            isReliable, textBytesFound, details = cld2.detect(srctxt, bestEffort=True)
            fromLang = details[0][1]
            print("language detected = " + fromLang)

        langpair = fromLang + '-' + toLang
        if not langpair in opusMT:
            print('unsupported language pair ' + langpair)
            self.sendMessage('ERROR: unsupported language pair ' + langpair)
            return

        server = opusMT[langpair]
        ws[server].send(langpair + ' ' + srctxt)
        print('translate ' + langpair + ' at ' + server)
        translated = ws[server].recv()
        self.sendMessage(translated)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')

server = SimpleWebSocketServer('', args.port, Translate)
server.serveforever()
