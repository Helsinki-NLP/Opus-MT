#!/usr/bin/env python3
#-*-python-*-
#
#

import signal
import sys
import argparse
import codecs
import json
import socket
import socketserver

# from websocket import create_connection
# from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket


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
    ws[h] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST, PORT = h.split(':')
    ws[h].connect((HOST, int(PORT)))
    srclangs = opusMT_servers[h]["source-languages"].split('+')
    trglangs = opusMT_servers[h]["target-languages"].split('+')
    for s in srclangs:
        for t in trglangs:
            print(" - serving " + s + t)
            opusMT[s+'-'+t] = h



class Translate(socketserver.BaseRequestHandler):
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

        langpair = fromLang + '-' + toLang
        if not langpair in opusMT:
            print('unsupported language pair ' + langpair)
            data = {'error': 'unsupported language pair ' + langpair,
                    'source': fromLang, 'target': toLang}
            self.request.sendall(bytes(json.dumps(data, sort_keys=True, indent=4), "utf-8"))
            return

        server = opusMT[langpair]

        data = {'text': srctext, 'source': fromLang, 'target': toLang}
        message = json.dumps(data, sort_keys=True, indent=4)
        print("sending to " + server + ":" + message)
        ws[server].sendall(bytes(message, "utf-8"))
        translated = ws[server].recv(1024)
        self.request.sendall(translated)



# Create the server, binding to localhost on port 9999
server = socketserver.TCPServer(("localhost", args.port), Translate)

# Activate the server; this will keep running until you
# interrupt the program with Ctrl-C
server.serve_forever()
