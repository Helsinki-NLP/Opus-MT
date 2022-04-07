#!/usr/bin/env python3
#-*-python-*-

import yaml
import sys

id=0
vocab={}
for line in sys.stdin:
    vocab[line.rstrip()] = id
    id+=1

print(yaml.dump(vocab, allow_unicode=True))
