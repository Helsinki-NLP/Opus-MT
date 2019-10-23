
# OPUS-MT

Tools and resources for open translation services

* based on MarianNMT
* trained on OPUS data
* [pre-trained downloadable translation models](http://opus.nlpl.eu/Opus-MT.php)

This repository includes

* scripts for training models (currently this only works in our work environment at CSC)
* A web application providing a web UI and api to work with multiple language pairs

## Installation

Download the latest version from github:

```bash
git clone https://github.com/Helsinki-NLP/Opus-MT.git
```

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

## Using Docker

```bash
docker-compose up
```

And launch your browser to localhost:8888

## Configuration

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

## Public MT models

We store public models at https://object.pouta.csc.fi/OPUS-MT
Check the files in `models/`. They should be all compatible with the OPUS-MT services and you can install them by specifying the language pair.

## Train MT models

There is a Makefile for training new models from OPUS data in `Opus-MT/train` but this is heavily customized for the work environment at CSC and the University of Helsinki projects. This will (hopefully) be more generic in the future to be able to run in different environments and setups as well.
