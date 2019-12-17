
# OPUS-MT

Tools and resources for open translation services

* based on MarianNMT
* trained on OPUS data
* [pre-trained downloadable translation models](https://github.com/Helsinki-NLP/Opus-MT/tree/master/train/models)


This repository includes two setups:

* Setup 1: a Tornado-based web application providing a web UI and api to work with multiple language pairs
* Setup 2: a simple websocket service setup with some experimental API extensions

There are also scripts for training models but those are currently only useful in the computing environment used by the University of Helsinki and CSC as the IT service providor.


## Installation of the Tornado-based Web-App

Download the latest version from github:

```bash
git clone https://github.com/Helsinki-NLP/Opus-MT.git
```

### Option 1: Manual setup

Install Marian MT. Follow the documentation at https://marian-nmt.github.io/docs/
After the installation, marian-server is expected to be present in path. If not place it in `/usr/local/bin`

Install pre-requisites.
Using a virtual environment is recommended.

```bash
pip install -r requirements.txt
```

Download the language models from http://opus.nlpl.eu/Opus-MT.php and place it in models directory.

Then edits the services.json to point to that models.

And start the webserver.
```bash
python server.py
```

By default, it will use port 8888. Launch your browser to localhost:8888 to get the web interface. The languages configured in services.json will be available.


### Option 2: Using Docker


```bash
docker-compose up
```

And launch your browser to localhost:8888


### Configuration

The server.py program accepts a configuration file in json format. By default it try to use `config.json` in the current directory. But you can give a custom one using `-c` flag.

An example configuration file looks like this:

```json
{
    "en": {
        "es": {
            "configuration": "./models/en-es/decoder.yml",
            "host": "localhost",
            "port": "10001"
        },
        "fi": {
            "configuration": "./models/en-fi/decoder.yml",
            "host": "localhost",
            "port": "10002"
        },
    }
}

```

This example configuration can provide MT service for en->fs and en->fi language pairs.

* `configuration` points to a yaml file containing the decoder configuration usable by `marian-server`. If this value is not provided, Opus-MT will assume that the service is already running in a remote host and post as given in other options. If value is provided a new sub process will be created using `marian-server`
* `host`: The host where the server is running.
* `port`: The port to be listen for `marian-server`







## Installation of a websocket service on Ubuntu

Download the latest version from github:

```bash
git clone https://github.com/Helsinki-NLP/Opus-MT.git
```

Install pre-requisites (tested on Ubuntu 14.04, 16.04 and 18.04, the installation requires sudo permissions):

```
cd Opus-MT/install
make all
sudo make install
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

`marian-opus-fi-en` is the service that runs the actual translation using marian-server. This is implemented as a websocket service that expects plain text input that has been pre-processed according to the model behind the server (i.e. may require tokenized, normalized and text segmented into BPE or other kinds of subword units). `opusMT-opus-fi-en status` does this kind of pre-processing also including sentence boundary detection. `opusMT` is a routing server that makes it possible to connect several translation servers. Translation servers need to be defined in a JSON file that is used as configuration.

If any of those servers do not run then try to restart them in this order:

```
sudo service marian-opus-fi-en restart
sudo service opusMT-opus-fi-en restart
sudo service opusMT restart
```

### Translating text

The translation service is provided as a websocket service. The `opusMT-client.py` implements a script that demonstrates how to call the API. Youe can test the service by piping plain text to the client script using the socket of the running server:

```
echo "Mitä kuuluu? Käännös on hauskaa." | ./opusMT-client.py -H localhost -P 20000 -s fi -t en
```

This should return something like

```
{
    "alignment": [
        "0-0 0-2 1-1 2-3",
        "0-0 1-1 3-2 4-3 5-4"
    ],
    "result": "How are you? The translation is fun.",
    "server": "192.168.1.18:20001",
    "source": "fi",
    "source-segments": [
        "Mit\u00e4 kuuluu ?",
        "K\u00e4\u00e4@@ nn\u00f6@@ s on hauskaa ."
    ],
    "source-sentences": [
        "Mit\u00e4 kuuluu?",
        "K\u00e4\u00e4nn\u00f6s on hauskaa."
    ],
    "target": "en",
    "target-segments": [
        "How are you ?",
        "The translation is fun ."
    ],
    "target-sentences": [
        "How are you?",
        "The translation is fun."
    ]
}
```

The final translation is returned in the `result` field. `source-segments` and `target-segments` show the individual sentences after pre-processing and before post-processing, respectively. The client script sends the request in JSON with `text` including the plain source language tect to be translated, `source` and `target` specifying the source and the target language (typically, iso-639-1 language IDs). `source` can also be set to `detect` or `DL` in order to use language identification to detect the input language.

The same format can be used to request translations from the opusMT routing server. If this service is running, several trabslation services can be connected via the same API. The service listens on port 8080 by default.

```
echo "Mitä kuuluu? Käännös on hauskaa." | ./opusMT-client.py -H localhost -P 8080 -s fi -t en
```

It returns an error message in the `result` field if the language pair is not supported.




### Setup other language pairs:


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

Edit the server configuration file `opusMT-servers.json` again to add the new service and restart the service. Each entry in the configuration file specifies a server running on some accessible machine. `localhost` is the local machine but other IP addresses can be listed here together with the port the translation server is listening at:

```
{
    "localhost:20000" : {
	"source-languages" : "fi",
	"target-languages" : "en"
    },
    "192.168.1.14:21100" : {
	"source-languages" : "fr",
	"target-languages" : "et+fi"
    }
}
```

Multilingual models are specified with language IDs separated by `+` characters. If certain language pairs are served with multiple services then you will need to specify model names to make it possible to select specific models in the request:

```
{
    "192.168.1.19:20004" : {
	"source-languages" : "de",
	"target-languages" : "fi"
    },
    "192.168.1.12:20008" : {
        "model" : "wmt",
	"source-languages" : "de",
	"target-languages" : "fi"
    }
}
```

The default name of a model is `default` (if no name is given) and each language pair should have at least one default model that will be called if no specific model is specified. Finally, update the installation and restart the service after editing the configuration file.


```
sudo make opusMT-router
sudo service opusMT restart
```

The default location of the configuration file is `/usr/local/share/opusMT/`.



## Public MT models

We store public models at https://object.pouta.csc.fi/OPUS-MT-models
They should be all compatible with the OPUS-MT services and you can install them by specifying the language pair. The installation script takes the latest model in that directory. For additional customisation you need to adjust the installation procedures (in the Makefile or elsewhere).




## Train MT models

There is a Makefile for training new models from OPUS data in `Opus-MT/train` but this is heavily customized for the work environment at CSC and the University of Helsinki projects. This will (hopefully) be more generic in the future to be able to run in different environments and setups as well.

