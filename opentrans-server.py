#!/usr/bin/env python3
#-*-python-*-
#
#

import codecs
import pycld2 as cld2
from mosestokenizer import *
from websocket import create_connection

from apply_bpe import BPE


#####################################################################
#### TODO:  all of this should be handled with command-line options!

port = 8080

## specify the server that runs marian-decoder
marian_server = 'localhost'
marian_port   = 11111

## languages that can be translated from and translated into
srclangs = ['de','fr','sv','en']
trglangs = ['et','hu','fi']
default_trg = 'fi'

## BPE model for pre-processing
BPEmodel = '/media/letsmt/nmt/models/de+fr+sv+en-et+hu+fi/opus-wmt.src.bpe32k-model'
BPEcodes = codecs.open(BPEmodel, encoding='utf-8')
bpe = BPE(BPEcodes)

################################################################


## pre- and post-processing tools
tokenizer = {}
sentence_splitter = {}
normalizer = {}
detokenizer = {}

for l in srclangs:
    sentence_splitter[l] = MosesSentenceSplitter(l)
    normalizer[l] = MosesPunctuationNormalizer(l)
    tokenizer[l] = MosesTokenizer(l)

for l in trglangs:
    detokenizer[l] = MosesDetokenizer(l)


# open connection
ws = create_connection("ws://{}:{}/translate".format(marian_server, marian_port))


from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class Translate(WebSocket):

    def handleMessage(self):

        fromLang = None
        toLang = default_trg
        prefix = ''

        ## check whether the first token specifies the language pair
        tokens = self.data.split()
        langs = tokens.pop(0).split('-')
        if len(langs) == 2:
            toLang = langs[1]
            if langs[0] != 'DL':
                fromLang = langs[0]
            self.data = ' '.join(tokens)

        if len(trglangs) > 1:
            prefix = '>>' + toLang + '<< '

        if not fromLang:
            isReliable, textBytesFound, details = cld2.detect(self.data, bestEffort=True)
            fromLang = details[0][1]
            print("language detected = " + fromLang)

        if not fromLang in srclangs:
            print('unsupported source language ' + fromLang)
            self.sendMessage('ERROR: unsupported source language ' + fromLang)
            return

        if not toLang in trglangs:
            print('unsupported target language ' + toLang)
            self.sendMessage('ERROR: unsupported target language ' + toLang)
            return

        message = []
        for s in sentence_splitter[fromLang]([normalizer[fromLang](self.data)]):
            # print(s)
            tokenized = ' '.join(tokenizer[fromLang](s))
            # print(tokenized)
            segmented = bpe.process_line(tokenized)
            # print(prefix + segmented)
            ws.send(prefix + segmented)
            translated = ws.recv().replace('@@ ','')
            # print(translated)
            detokenized = detokenizer[toLang](translated.split())
            print('TRANSLATION: ' + detokenized)
            message.append(detokenized)
        self.sendMessage(' '.join(message))

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')

server = SimpleWebSocketServer('', port, Translate)
server.serveforever()
