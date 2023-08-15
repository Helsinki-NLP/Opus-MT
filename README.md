
<img src="https://github.com/Helsinki-NLP/Opus-MT/blob/master/img/opus_mt.png" width="250" alt="OPUS-MT"/>


Tools and resources for open translation services

* based on [Marian-NMT](https://marian-nmt.github.io/)
* trained on [OPUS](http://opus.nlpl.eu/) data using [OPUS-MT-train](https://github.com/Helsinki-NLP/Opus-MT-train) (New: [leaderboard](https://opus.nlpl.eu/leaderboard/))
* mainly [SentencePiece](https://github.com/google/sentencepiece)-based segmentation
* mostly trained with guided alignment based on [eflomal](https://github.com/robertostling/eflomal) wordalignments 
* [pre-trained downloadable translation models](https://github.com/Helsinki-NLP/Opus-MT-train/tree/master/models) ([matrix view](http://opus.nlpl.eu/Opus-MT/)), CC-BY 4.0 license
* [more freely available translation models](https://github.com/Helsinki-NLP/Tatoeba-Challenge/blob/master/results/tatoeba-results-all.md) from the [Tatoeba translation challenge](https://github.com/Helsinki-NLP/Tatoeba-Challenge), CC-BY 4.0 license
* demo translation interface available from https://opusmt.wmflabs.org/
* 543 live demo APIs of language variants available at [Tiyaro.ai](https://console.tiyaro.ai/explore?q=opus-mt&pub=Helsinki-NLP).  For example, an [English to German finetuned translator](https://console.tiyaro.ai/explore/Helsinki-NLP-opus-mt-en-de/demo)

<p>
<a href="https://console.tiyaro.ai/explore?q=opus-mt&pub=Helsinki-NLP"> <img src="https://tiyaro-public-docs.s3.us-west-2.amazonaws.com/assets/try_on_tiyaro_badge.svg"></a>
</p>


This repository includes two setups:

* Setup 1: a [Tornado](https://www.tornadoweb.org)-based web application providing a web UI and API to work with multiple language pairs (developed by [Santhosh Thottingal](https://github.com/santhoshtr) and his team at the Wikimedia Foundation); an example instance is available here: https://opusmt.wmflabs.org/
* Setup 2: [a simple websocket service setup with some experimental API extensions](https://github.com/Helsinki-NLP/Opus-MT/tree/master/doc/WebSocketServer.md)

There are also [scripts for training models](https://github.com/Helsinki-NLP/Opus-MT-train), but those are currently only useful in the computing environment used by the University of Helsinki and CSC as the IT service provider.

Please cite the following paper if you use OPUS-MT software and models:

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
After the installation, marian-server is expected to be present in path. If not, place it in `/usr/local/bin`

Install pre-requisites.
Using a virtual environment is recommended.

```bash
pip install -r requirements.txt
```

Download the translation models from https://github.com/Helsinki-NLP/Opus-MT-train/tree/master/models and place them in models directory.

Then edit the services.json to point to those models.

And start the webserver.
```bash
python server.py
```

By default, it will use port 8888. Launch your browser to localhost:8888 to get the web interface. The languages configured in services.json will be available.

### Option 2: Using Docker

```bash
docker-compose up
```

or

```bash
docker build . -t opus-mt
docker run -p 8888:8888 opus-mt:latest
```

And launch your browser to localhost:8888

#### Option 2.1: Using Docker with CUDA GPU

```bash
docker build -f Dockerfile.gpu . -t opus-mt-gpu
nvidia-docker run -p 8888:8888 opus-mt-gpu:latest
```

And launch your browser to localhost:8888

### Configuration

The server.py program accepts a configuration file in json format. By default it try to use `services.json` in the current directory. But you can give a custom one using `-c` flag.

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

This example configuration can provide MT service for en->es and en->fi language pairs.

* `configuration` points to a yaml file containing the decoder configuration usable by `marian-server`. If this value is not provided, Opus-MT will assume that the service is already running in a remote host and post as given in other options. If value is provided, a new subprocess will be created using `marian-server`
* `host`: The host where the server is running.
* `port`: The port to be listen for `marian-server`




## Installation of a websocket service on Ubuntu

There is another option of setting up translation services using WebSockets and Linux services. Detailed information is available from 
[doc/WebSocketServer.md](https://github.com/Helsinki-NLP/Opus-MT/tree/master/doc/WebSocketServer.md).


## Public MT models

We store public models (CC-BY 4.0 License) at https://github.com/Helsinki-NLP/Opus-MT-train/tree/master/models
They should all be compatible with the OPUS-MT services, and you can install them by specifying the language pair. The installation script takes the latest model in that directory. For additional customisation you need to adjust the installation procedures (in the Makefile or elsewhere).

There are also development versions of models, which are often a bit more experimental and of low quality. But there are additional language pairs and they can be downloaded from https://github.com/Helsinki-NLP/Opus-MT-train/tree/master/work-spm/models



## Train MT models

There is a Makefile for training new models from OPUS data in the [Opus-MT-train](https://github.com/Helsinki-NLP/Opus-MT-train) repository, but this is heavily customized for the work environment at CSC and the University of Helsinki projects. This will (hopefully) be more generic in the future to be able to run in different environments and setups as well.


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


## Links and related work

* [OPUS-translator](https://github.com/Helsinki-NLP/OPUS-translator): implementation of a simple on-line translation interface
* [OPUS-CAT](https://github.com/Helsinki-NLP/OPUS-CAT): an implementation of an NMT plugin for Trados Studio that can run OPUS-MT models
* [fiskmö](https://blogs.helsinki.fi/fiskmo-project/): a project on the devlopment of resources and tools for translating between Finnish and Swedish
* [The Tatoeba MT Challenge](https://github.com/Helsinki-NLP/Tatoeba-Challenge/) with [lots of pre-trained NMT models](https://github.com/Helsinki-NLP/Tatoeba-Challenge/blob/master/results/tatoeba-results-all.md)
* [The NMT map](https://opus.nlpl.eu/NMT-map/Tatoeba/all/src2trg/) that plots the status of Tatoeba NMT models on a map
* [The OPUS-MT leaderboard](https://opus.nlpl.eu/leaderboard/)
* [pre-trained multilingual models](https://github.com/bzhangGo/zero/tree/master/docs/multilingual_laln_lalt#pretrained-multilingual-models-many-to-many) trained on [OPUS-100](https://github.com/EdinburghNLP/opus-100-corpus) using the [zero](https://github.com/bzhangGo/zero) toolkit


## Acknowledgements

The work is supported by the [European Language Grid](https://www.european-language-grid.eu/) as [pilot project 2866](https://live.european-language-grid.eu/catalogue/#/resource/projects/2866), by the [FoTran project](https://www.helsinki.fi/en/researchgroups/natural-language-understanding-with-cross-lingual-grounding), funded by the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation programme (grant agreement No 771113), and the [MeMAD project](https://memad.eu/), funded by the European Union’s Horizon 2020 Research and Innovation Programme under grant agreement No 780069. We are also grateful for the generous computational resources and IT infrastructure provided by [CSC -- IT Center for Science](https://www.csc.fi/), Finland.
