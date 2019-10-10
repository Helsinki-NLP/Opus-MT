
# OPUS-MT

Tools and resources for open translation services

* based on MarianNMT
* trained on OPUS data
* [pre-trained downloadable translation models](http://opus.nlpl.eu/Opus-MT.php)


This repository includes

* scripts for training models (currently this only works in our work environment at CSC)
* installation of the pre-requisites on Ubuntu 14.04 or 16.04
* server and client scripts for OPUS-MT services


## Installation

Download the latest version from github:

```
git clone https://github.com/Helsinki-NLP/Opus-MT.git
```

Install pre-requisites (tested on Ubuntu 14.04 and 16.04, the installation requires sudo permissions):

```
cd Opus-MT/install
make all
cd ../..
```

Install the MT-server (for Finnish-English):

```
cd Opus-MT
sudo make all
```


Make sure that the services are running (change language IDs in the name if necessary):

```
service marian-opus-fi-en status
service opusMT-opus-fi-en status
service opusMT status
```


Restart them in this order if they are not running:

```
sudo service marian-opus-fi-en restart
sudo service opusMT-opus-fi-en restart
sudo service opusMT restart
```


## Setup other language pairs:


Set SRC_LANGS, TRG_LANGS, MARIAN_PORT and OPUSMT_PORT.
For example, for installing a server that handles English input and translates to Finnish:

```
sudo make SRC_LANGS=en TRG_LANGS=fi MARIAN_PORT=10001 OPUSMT_PORT=20001 opusMT-server
```

You can also look at the other exampels in the Makefile.
Edit `opusMT-servers.json` by adding the additional services and re-install the opusMT service:

```
sudo make opusMT-router
sudo service marian-opus-en-fi restart
sudo service opusMT-opus-en-fi restart
sudo service opusMT restart
```

Multilingual models are possible as well. For example, to install a model that is able to translate from German, Afrikaans, Frisian and Dutch to either Estonian or Finnish can be installed by running:


```
sudo make SRC_LANGS="de+af+fy+nl" TRG_LANGS="et+fi" MARIAN_PORT=10002 OPUSMT_PORT=20002 opusMT-server
sudo service marian-opus-de+af+fy+nl-et+fi restart
sudo service opusMT-opus-de+af+fy+nl-et+fi restart
```

Edit the server configuration file `opusMT-servers.json` again to add the new service and restart the service:

```
sudo make opusMT-router
sudo service opusMT restart
```





## Public MT models

We store public models at https://object.pouta.csc.fi/OPUS-MT
Check the files in `models/`. They should be all compatible with the OPUS-MT services and you can install them by specifying the language pair. The installation script takes the latest model in that directory. For additional customisation you need to adjust the installation procedures (in the Makefile or elsewhere).




## Train MT models

There is a Makefile for training new models from OPUS data in `Opus-MT/train` but this is heavily customized for the work environment at CSC and the University of Helsinki projects. This will (hopefully) be more generic in the future to be able to run in different environments and setups as well.

