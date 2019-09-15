#!/usr/bin/python3
#-*-python-*-
#
#

import time
import signal
import sys
import argparse
import codecs
import json
import socketserver
from websocket import create_connection


## pre-processing: 
## - moses-script wrapper classes
## - BPE-based segmentation from subword-nmt
from apply_bpe import BPE
from mosestokenizer import *

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
parser.add_argument('--bpe','--bpe-model', type=str, default='opus.de+fr+sv+en.bpe32k-model',
                    help='BPE model for source text segmentation')
parser.add_argument('-c','--cache', type=str, default='opentrans-cache.db',
                    help='BPE model for source text segmentation')


args = parser.parse_args()


if not args.deftrg: 
    args.deftrg = args.trglangs[0]



## BPE model for pre-processing
print("load BPE codes")
BPEcodes = codecs.open(args.bpe, encoding='utf-8')
bpe = BPE(BPEcodes)


## open the cache DB
print("open cache")
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

print("start pre- and post-processing tools")
for l in args.srclangs:
    sentence_splitter[l] = MosesSentenceSplitter(l)
    normalizer[l] = MosesPunctuationNormalizer(l)
    tokenizer[l] = MosesTokenizer(l)

for l in args.trglangs:
    detokenizer[l] = MosesDetokenizer(l)


# open connection
print("open connection to " + args.mthost)
ws = create_connection("ws://{}:{}/translate".format(args.mthost, args.mtport))


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.request.recv(1024).strip().decode('utf-8')
        
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)

        ## TODO: verify proper JSON input
        data = json.loads(self.data)
        fromLang = None
        toLang = args.deftrg

        if 'source' in data:
            if data['source'] != 'detect':
                fromLang = data['source']
        if 'target' in data:
            if data['target']:
                toLang = data['target']

        prefix = ''

        ## check the cache first
        if self.data in cache:
            translation = cache[self.data]
            print('CACHED TRANSLATION: ' + translation)
            data = {'result': translation, 'origin': 'cache'}
            self.request.sendall(bytes(json.dumps(data, sort_keys=True, indent=4), "utf-8"))
            # self.request.sendall(bytes(translation, "utf-8"))
            return

        if len(args.trglangs) > 1:
            prefix = '>>' + toLang + '<< '

        if not fromLang:
            isReliable, textBytesFound, details = cld2.detect(data['text'], bestEffort=True)
            fromLang = details[0][1]
            print("language detected = " + fromLang)

        if not fromLang in args.srclangs:
            print('unsupported source language ' + fromLang)
            data = {'error': 'unsupported source language ' + fromLang,
                    'source': fromLang, 'target': toLang}
            self.request.sendall(bytes(json.dumps(data, sort_keys=True, indent=4), "utf-8"))
            # self.request.sendall(bytes('ERROR: unsupported source language ' + fromLang, "utf-8"))
            return

        if not toLang in args.trglangs:
            print('unsupported target language ' + toLang)
            data = {'error': 'unsupported target language ' + toLang,
                    'source': fromLang, 'target': toLang}
            self.request.sendall(bytes(json.dumps(data, sort_keys=True, indent=4), "utf-8"))
            # self.request.sendall(bytes('ERROR: unsupported target language ' + toLang, "utf-8"))
            return

        langpair = fromLang + toLang
        message = []
        for s in sentence_splitter[fromLang]([normalizer[fromLang](data['text'])]):
            key = langpair + ' ' + s
            if key in cache:
                detokenized = cache[key]
                print('CACHED TRANSLATION: ' + detokenized)
            else:
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
            cache[key] = detokenized
        trgtext = ' '.join(message)
        data = {'result': trgtext, 'source': fromLang, 'target': toLang,
                'origin': "ws://{}:{}/translate".format(args.mthost, args.mtport)}
        self.request.sendall(bytes(json.dumps(data, sort_keys=True, indent=4), "utf-8"))
        # self.request.sendall(bytes(trgtext, "utf-8"))
        cache[self.data] = trgtext



if __name__ == "__main__":
    HOST, PORT = "localhost", args.port

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
