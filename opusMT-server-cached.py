#!/usr/bin/python3
#-*-python-*-
#
#

from __future__ import print_function, unicode_literals, division

import time
import signal
import sys
import argparse
import codecs
import json
# import socketserver
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from websocket import create_connection


## pre-processing: 
## - moses-script wrapper classes
## - BPE-based segmentation from subword-nmt
## - sentencepiece
from apply_bpe import BPE
from mosestokenizer import *
import sentencepiece as spm

## language identifer (if source language is not given)
import pycld2 as cld2

## for the cache
## --> unlimited size
## --> assumes that translations from the server don't change
from sqlitedict import SqliteDict

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
parser.add_argument('--bpe','--bpe-model', type=str,
                    help='BPE model for source text segmentation')
parser.add_argument('--spm','--sentence-piece-model', type=str,
                    help='sentence piece model for source text segmentation')
parser.add_argument('-c','--cache', type=str, default='opusMT-cache.db',
                    help='BPE model for source text segmentation')


args = parser.parse_args()


if not args.deftrg: 
    args.deftrg = args.trglangs[0]



## load BPE model for pre-processing
if args.bpe:
    print("load BPE codes from " + args.bpe, flush=True)
    BPEcodes = codecs.open(args.bpe, encoding='utf-8')
    bpe = BPE(BPEcodes)

## load SentencePiece model for pre-processing
if args.spm:
    print("load sentence piece model from " + args.spm, flush=True)
    spm = spm.SentencePieceProcessor()
    spm.Load(args.spm)


## open the cache DB
print("open cache at " + args.cache, flush=True)
cache = SqliteDict(args.cache, autocommit=True)


## add signal handler for SIGINT to properly close 
## the DB when interrupting
def signal_handler(sig, frame):
    cache.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


## pre- and post-processing tools
tokenizer = {}
sentence_splitter = {}
normalizer = {}
detokenizer = {}

## TODO: should we have support for other sentence splitters?
print("start pre- and post-processing tools")
for l in args.srclangs:
    sentence_splitter[l] = MosesSentenceSplitter(l)
    normalizer[l] = MosesPunctuationNormalizer(l)
    if args.bpe:
        tokenizer[l] = MosesTokenizer(l)

if args.bpe:
    for l in args.trglangs:
        detokenizer[l] = MosesDetokenizer(l)


# open connection
print("open connection to " + args.mthost + " at port " + str(args.mtport), flush=True)
ws = create_connection("ws://{}:{}/translate".format(args.mthost, args.mtport))


class Translate(WebSocket):

    def handleMessage(self):

        prefix = ''
        fromLang = None
        toLang = args.deftrg
        # print('received: ' + self.data, flush=True)

        ## check whether we retrieve a JSON string or not
        try:
            data = json.loads(self.data)
            srctxt = data['text']
            if 'source' in data:
                if data['source'] != 'detect':
                    fromLang = data['source']
            if 'target' in data:
                if data['target']:
                    toLang = data['target']
        except ValueError as error:
            print("invalid json: %s" % error)
            srctxt = self.data
            # check whether first token indiciates language pair
            tokens = srctxt.split()
            langs = tokens.pop(0).split('-')
            if len(langs) == 2:
                toLang = langs[1]
                if langs[0] != 'DL' and langs[0] != 'detect':
                    fromLang = langs[0]
                srctxt = " ".join(tokens)

        if len(args.trglangs) > 1:
            prefix = '>>' + toLang + '<< '

        ## check the cache first
        # print('input: ' + srctxt, flush=True)
        inputTxt = prefix + srctxt
        if inputTxt in cache:
            cached = cache[inputTxt].split("\t")
            translation = cached[0]
            print('CACHED TRANSLATION: ' + translation, flush=True)
            data = {'result': translation, 'origin': 'cache'}

            if len(cached) == 4:
                data['source-segments'] = [cached[1]]
                data['target-segments'] = [cached[2]]
                data['alignment'] = [cached[3]]
                if args.bpe:
                    data['source-sentences'] = [srctxt]
                    data['target-sentences'] = [translation]
                    data['segmentation'] = 'bpe'
                else:
                    data['segmentation'] = 'spm'

            self.sendMessage(json.dumps(data, sort_keys=True, indent=4))
            return

        if not fromLang:
            isReliable, textBytesFound, details = cld2.detect(srctxt, bestEffort=True)
            fromLang = details[0][1]
            print("language detected = " + fromLang, flush=True)

        if not fromLang in args.srclangs:
            print('unsupported source language ' + fromLang, flush=True)
            data = {'error': 'unsupported source language ' + fromLang,
                    'source': fromLang, 'target': toLang}
            self.sendMessage(json.dumps(data, sort_keys=True, indent=4))
            return

        if not toLang in args.trglangs:
            print('unsupported target language ' + toLang, flush=True)
            data = {'error': 'unsupported target language ' + toLang,
                    'source': fromLang, 'target': toLang}
            self.sendMessage(json.dumps(data, sort_keys=True, indent=4))
            return

        langpair = fromLang + toLang
        sentSourceBPE = []
        sentTranslated = []
        sentTranslatedTokenized = []
        sentTranslatedBPE = []
        sentAlignment = []
        sentSource = sentence_splitter[fromLang]([normalizer[fromLang](srctxt)])

        # for s in sentence_splitter[fromLang]([normalizer[fromLang](srctxt)]):
        for s in sentSource:
            key = langpair + ' ' + s
            if key in cache:
                cached = cache[key].split("\t")
                sentTranslated.append(cached[0])
                if len(cached) == 4:
                    sentSourceBPE.append(cached[1])
                    sentTranslatedBPE.append(cached[2])
                    sentAlignment.append(cached[3])
                print('CACHED TRANSLATION: ' + cached[0], flush=True)
            else:
                if args.bpe:
                    # print('raw sentence: ' + s, flush=True)
                    tokenized = ' '.join(tokenizer[fromLang](s))
                    # print('tokenized sentence: ' + tokenized, flush=True)
                    segmented = bpe.process_line(tokenized)
                elif args.spm:
                    # print('raw sentence: ' + s, flush=True)
                    segmented = ' '.join(spm.EncodeAsPieces(s))
                    # print(segmented, flush=True)
                else:
                    segmented = s

                # print('segmented sentence ' + prefix + segmented, flush=True)
                ws.send(prefix + segmented)
                # print('successfully sent', flush=True)
                received = ws.recv().strip().split(' ||| ')
                # print(received, flush=True)

                ## undo segmentation
                if args.bpe:
                    translated = received[0].replace('@@ ','')
                elif args.spm:
                    translated = received[0].replace(' ','').replace('▁',' ').strip()
                    # translated = sp.DecodePieces(received[0].split(' '))
                else:
                    translated = received[0].strip()

                alignment = ''
                if len(received) == 2:
                    alignment = received[1]
                    links = alignment.split(' ')
                    fixedLinks = []
                    inputLength = len(segmented.split(' '))
                    outputLength = len(received[0].split(' '))
                    for link in links:
                        ids = link.split('-')
                        ## change the source IDs if there is a lang-ID prefix
                        if prefix != '':
                            ids[0] = str(int(ids[0])-1)
                        if ids[0] != '-1' and int(ids[0])<inputLength:
                            if int(ids[1])<outputLength:
                                fixedLinks.append('-'.join(ids))
                    alignment = ' '.join(fixedLinks)

                if args.bpe:
                    detokenized = detokenizer[toLang](translated.split())
                else:
                    detokenized = translated

                print('TRANSLATION: ' + detokenized, flush=True)
                sentSourceBPE.append(segmented)
                sentTranslatedBPE.append(received[0])
                sentAlignment.append(alignment)
                sentTranslated.append(detokenized)
                
                cache[key] = detokenized + "\t" + segmented + "\t" + received[0] + "\t" + alignment
                
        trgtext = ' '.join(sentTranslated)
        data = {'result': trgtext, 'source': fromLang, 'target': toLang,
                'source-segments': sentSourceBPE, 'target-segments': sentTranslatedBPE,
                'alignment' : sentAlignment }
        if args.bpe:
            data['source-sentences'] = sentSource
            data['target-sentences'] = sentTranslated
            data['segmentation'] = 'bpe'
        else:
            data['segmentation'] = 'spm'

        # 'origin': "ws://{}:{}/translate".format(args.mthost, args.mtport)}
        self.sendMessage(json.dumps(data, sort_keys=True, indent=4))

        ## TODO: we should also store alignments and source segments for the whole text
        # if not inputTxt in cache:
        #     cache[inputTxt] = trgtext

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')





print("listen on socket " + str(args.port))
server = SimpleWebSocketServer('', args.port, Translate)
server.serveforever()

