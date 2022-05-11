#!/usr/bin/env python3

from __future__ import print_function, unicode_literals, division

import sys
import ssl
import time
import argparse
import json

from websocket import create_connection


if __name__ == "__main__":
    # handle command-line options
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--batch-size", type=int, default=1)
    parser.add_argument("-H", "--host", type=str, default='86.50.168.81')
    parser.add_argument("-P", "--port", type=int, default=8080)
    parser.add_argument('-T', '--text', dest='text', action='store_true')
    parser.add_argument("-s", "--source-language", type=str, default='detect')
    parser.add_argument("-t", "--target-language", type=str, default='en')
    parser.add_argument("-m", "--model", type=str, default='default')
    parser.add_argument("--ssl", default=0, type=int, action="store", dest="ssl",
                  help="ssl (1: on, 0: off (default))")
    
    args = parser.parse_args()

    # open connection
    if args.ssl == 1:
        ws = create_connection("wss://{}:{}/translate".format(args.host,args.port), sslopt={"cert_reqs": ssl.CERT_NONE})

    else:
        ws = create_connection("ws://{}:{}/translate".format(args.host,args.port))

    count = 0
    batch = ""
    for line in sys.stdin:
        # print("received line " + line)
        count += 1
        batch += line.decode('utf-8') if sys.version_info < (3, 0) else line
        if count == args.batch_size:
            # translate the batch
            data = {'text': batch, 'source': args.source_language, 'target': args.target_language, 'model': args.model}
            # print("send batch " + json.dumps(data))
            ws.send(json.dumps(data))
            # print("send batch " + batch)
            # langpair = args.source_language + '-' + args.target_language
            # ws.send(langpair + ' ' + batch)
            result = ws.recv()
            if args.text:
                record = json.loads(result)
                print(record['result'])
            else:
                print(result.rstrip())

            count = 0
            batch = ""

    if count:
        # translate the remaining sentences
        # print("send batch " + batch)
        data = {'text': batch, 'source': args.source_language, 'target': args.target_language}
        ws.send(json.dumps(data))
        # 'origin': "ws://{}:{}/translate".format(args.mthost, args.mtport)}
        # ws.send(batch)
        # langpair = args.source_language + '-' + args.target_language
        # ws.send(langpair + ' ' + batch)
        result = ws.recv()
        if args.text:
            json = json.loads(result)
            print(json['result'])
        else:
            print(result.rstrip())

    # close connection
    ws.close()
