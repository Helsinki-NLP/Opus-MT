
# OpenTrans

Tools for open translation services

* based on MarianNMT
* trained on OPUS data



## Setup


* Start a marian-server with the model that you want to support

```
~/marian/build/marian-server -p 11111 -b2 -n1 -m /media/letsmt/nmt/models/de+fr+sv+en-et+hu+fi/opus-wmt.bpe32k-bpe32k.enfi.transformer.model1.npz.best-perplexity.npz -v /media/letsmt/nmt/models/de+fr+sv+en-et+hu+fi/opus-wmt.bpe32k-bpe32k.enfi.vocab.yml /media/letsmt/nmt/models/de+fr+sv+en-et+hu+fi/opus-wmt.bpe32k-bpe32k.enfi.vocab.yml
```

* edit the translation server script and start it as well
# access from a client

