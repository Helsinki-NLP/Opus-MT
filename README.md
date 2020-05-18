<img src="https://github.com/Helsinki-NLP/Opus-MT/blob/master/img/opus_mt.png" width="250" alt="OPUS-MT"/>

Tools and resources for open translation services

* based on [Marian-NMT](https://marian-nmt.github.io/)
* trained on [OPUS](http://opus.nlpl.eu/) data using [OPUS-MT-train](https://github.com/Helsinki-NLP/Opus-MT-train)
* mainly [SentencePiece](https://github.com/google/sentencepiece)-based segmentation
* mostly trained with guided alignment based on [eflomal](https://github.com/robertostling/eflomal) wordalignments 
* [pre-trained downloadable translation models](https://github.com/Helsinki-NLP/Opus-MT-train/tree/master/models) ([matrix view](http://opus.nlpl.eu/Opus-MT/)), CC-BY 4.0 license
* demo translation interface available from https://opusmt.wmflabs.org/


This repository includes two setups:

* Setup 1: a [Tornado](https://www.tornadoweb.org)-based web application providing a web UI and api to work with multiple language pairs (developed by [Santhosh Thottingal](https://github.com/santhoshtr) and his team at the wikimedia foundation); en example instance is available here: https://opusmt.wmflabs.org/
* Setup 2: [a simple websocket service setup with some experimental API extensions](https://github.com/Helsinki-NLP/Opus-MT/tree/master/doc/WebSocketServer.md)

There are also [scripts for training models](https://github.com/Helsinki-NLP/Opus-MT-train) but those are currently only useful in the computing environment used by the University of Helsinki and CSC as the IT service providor.

There is no dedicated publication yet about OPUS-MT but, please, cite the following paper if you find the software and the models useful:

```
@InProceedings{TiedemannThottingal:EAMT2020,
  author = {J{\"o}rg Tiedemann and Santhosh Thottingal},
  title = {{OPUS-MT} — {B}uilding open translation services for the {W}orld},
  booktitle = {Proceedings of the 22nd Annual Conferenec of the European Association for Machine Translation (EAMT)},
  year = {2020},
  address = {Lisbon, Portugal}
 }
 ```

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

Download the translation models from https://github.com/Helsinki-NLP/Opus-MT-train/tree/master/models and place it in models directory.

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

There is another option of setting up translation services using WebSockets and Linux services. Detailed information is available from 
[doc/WebSocketServer.md](https://github.com/Helsinki-NLP/Opus-MT/tree/master/doc/WebSocketServer.md).


## Public MT models

We store public models (CC-BY 4.0 License) at https://github.com/Helsinki-NLP/Opus-MT-train/tree/master/models
They should be all compatible with the OPUS-MT services and you can install them by specifying the language pair. The installation script takes the latest model in that directory. For additional customisation you need to adjust the installation procedures (in the Makefile or elsewhere).

There are also development versions of models, which are often a bit more experimental and of low quality. But there are additional language pairs and they can be downloaded from https://github.com/Helsinki-NLP/Opus-MT-train/tree/master/work-spm/models



## Train MT models

There is a Makefile for training new models from OPUS data in the [Opus-MT-train](https://github.com/Helsinki-NLP/Opus-MT-train) repository but this is heavily customized for the work environment at CSC and the University of Helsinki projects. This will (hopefully) be more generic in the future to be able to run in different environments and setups as well.


## Known issues

* most automatic evaluations are made on simple and short sentences from the Tatoeba data collection; those scores will be too optimistic when running the models with other more realistic data sets
* Some (older) test results are not reliable as they use software localisation data (namely GNOME system messages) with a large overlap with other localisation data (i.e. Ubuntu system messages) that are included in the training data
* All current models are trained without filtering, data augmentation (like backfanslation) and domain adaptation and other optimisation procedures; there is no quality control besides of the automatic evaluation based on automatically selected test sets; for some language pairs there are at least also benchmark scores from official WMT test sets
* Most models are trained with a maximum of 72 training hours on 1 or 4 GPUs; not all of them converged before this time limit
* Validation and early stopping is based on automatically selected validation data, often from Tatoeba; the validation data is not representative for many applications


## To-Do and wish list

* more languages and language pairs
* better and more multilingual models
* optimize translation performance
* add backtranslation data
* domain-specific models
* GPU enabled container
* dockerized fine-tuning
* document-level models
* load-balancing and other service optimisations
* public MT service network
* feedback loop and personalisation


## Links

* [OPUS-translator](https://github.com/Helsinki-NLP/OPUS-translator): implementation of a simple on-line translation interface
* [fiskmö](https://blogs.helsinki.fi/fiskmo-project/): a project on the devlopment of resources and tools for translating between Finnish and Swedish
* [fiskmö-trados](https://github.com/Helsinki-NLP/fiskmo-trados): an implementation of an NMT plugin for Trados Studio that can run OPUS-MT models


## Acknowledgements

The work is supported by the [FoTran project](https://www.helsinki.fi/en/researchgroups/natural-language-understanding-with-cross-lingual-grounding), funded by the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation programme (grant agreement No 771113), and the [MeMAD project](https://memad.eu/), funded by the European Union’s Horizon 2020 Research and Innovation Programme under grant agreement No 780069. We are also greatful for the generous computational resources provided by [CSC -- IT Center for Science](https://www.csc.fi/), Finland.
