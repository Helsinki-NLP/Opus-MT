#!/usr/bin/env python3
#-*-python-*-
#
#

import argparse
import codecs
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
parser.add_argument('-mth','--mthost','--mt-server-host', type=str, default='localhost',
                   help='host of the MT server')
parser.add_argument('-mtp','--mtport','--mt-server-port', type=int, default=11111,
                   help='port of the MT server')
parser.add_argument('-s','--srclangs', metavar='srclangs', type=str, nargs='+',
                    default=['de','fr','sv','en'],
                    help='supported source languages')
parser.add_argument('-t','--trglangs', metavar='trglangs',type=str, nargs='+',
                    default=['fi','et','hu'],
                    help='supported source languages')
parser.add_argument('-d','--deftrg','--default-target-language', type=str,
                    help='default target language (for multilingual models)')
parser.add_argument('--bpe','--bpe-model', type=str, default='opus.de+fr+sv+en.bpe32k-model',
                    help='BPE model for source text segmentation')


args = parser.parse_args()


if not args.deftrg: 
    args.deftrg = args.trglangs[0]



## BPE model for pre-processing
BPEcodes = codecs.open(args.bpe, encoding='utf-8')
bpe = BPE(BPEcodes)



## pre- and post-processing tools
tokenizer = {}
sentence_splitter = {}
normalizer = {}
detokenizer = {}

for l in args.srclangs:
    sentence_splitter[l] = MosesSentenceSplitter(l)
    normalizer[l] = MosesPunctuationNormalizer(l)
    tokenizer[l] = MosesTokenizer(l)

for l in args.trglangs:
    detokenizer[l] = MosesDetokenizer(l)


# open connection
ws = create_connection("ws://{}:{}/translate".format(args.mthost, args.mtport))


class Translate(WebSocket):

    def handleMessage(self):

        fromLang = None
        toLang = args.deftrg
        prefix = ''

        ## check whether the first token specifies the language pair
        tokens = self.data.split()
        langs = tokens.pop(0).split('-')
        if len(langs) == 2:
            toLang = langs[1]
            if langs[0] != 'DL':
                fromLang = langs[0]
            self.data = ' '.join(tokens)

        if len(args.trglangs) > 1:
            prefix = '>>' + toLang + '<< '

        if not fromLang:
            isReliable, textBytesFound, details = cld2.detect(self.data, bestEffort=True)
            fromLang = details[0][1]
            print("language detected = " + fromLang)

        if not fromLang in args.srclangs:
            print('unsupported source language ' + fromLang)
            self.sendMessage('ERROR: unsupported source language ' + fromLang)
            return

        if not toLang in args.trglangs:
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

server = SimpleWebSocketServer('', args.port, Translate)
server.serveforever()
