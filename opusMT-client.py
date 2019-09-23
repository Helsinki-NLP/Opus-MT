#!/usr/bin/env python3

from __future__ import print_function, unicode_literals, division

import sys
import time
import argparse
import json

from websocket import create_connection


if __name__ == "__main__":
    # handle command-line options
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--batch-size", type=int, default=1)
    parser.add_argument("-s", "--host", type=str, default='86.50.168.81')
    parser.add_argument("-p", "--port", type=int, default=8080)
    parser.add_argument('-t', '--text', dest='text', action='store_true')
    args = parser.parse_args()

    # open connection
    ws = create_connection("ws://{}:{}/translate".format(args.host,args.port))

    count = 0
    batch = ""
    for line in sys.stdin:
        # print("received line " + line)
        count += 1
        batch += line.decode('utf-8') if sys.version_info < (3, 0) else line
        if count == args.batch_size:
            # translate the batch
            # print("send batch " + batch)
            ws.send(batch)
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
        print("send batch " + batch)
        ws.send(batch)
        result = ws.recv()
        if args.text:
            json = json.loads(result)
            print(json['result'])
        else:
            print(result.rstrip())

    # close connection
    ws.close()
