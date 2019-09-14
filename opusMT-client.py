#!/usr/bin/env python3


import socket
import sys
import json
import argparse

# handle command-line options
parser = argparse.ArgumentParser()
parser.add_argument("-b", "--batch-size", type=int, default=1)
parser.add_argument("-s", "--host", type=str, default='86.50.168.81')
parser.add_argument("-p", "--port", type=int, default=8080)
args = parser.parse_args()

HOST, PORT = args.host, args.port

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        for line in sys.stdin:
                fromLang = None
                toLang = None

                # check whether first token indiciates language pair
                tokens = line.split()
                langs = tokens.pop(0).split('-')
                if len(langs) == 2:
                        toLang = langs[1]
                        if langs[0] != 'DL':
                                fromLang = langs[0]
                                line = " ".join(tokens)
                                
                data = {'text': line, 'source': fromLang, 'target': toLang}
                message = json.dumps(data, sort_keys=True, indent=4)
                print("sending " + message)
                sock.sendall(bytes(message, "utf-8"))

                # Receive data from the server and shut down
                received = str(sock.recv(1024), "utf-8")
                print(received)
finally:
        sock.close()

