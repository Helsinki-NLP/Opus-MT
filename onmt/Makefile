

## example for starting an OpenNMT-py server hosted through OPUS-MT
## using the model trained for AmericasNLP 2021
## see https://zenodo.org/record/4906353


ZENODO_HOME = https://zenodo.org/record/4906353/files

## start the AmericasNLP 2021 model
.PHONY: all
all: americasnlp2021-onmt.log americasnlp2021-opusMT.log

## start the OpenNMT-py server
americasnlp2021-onmt.log: americasnlp2021.json OpenNMT-py modelB-100dev-170k.pt
	nohup python3 OpenNMT-py/server.py -c $< >> $@ &

## start the OPUS-MT wrapper
americasnlp2021-opusMT.log: sp-12lang-32k.spm
	nohup python3 opusMT-onmt-server.py -p 5001 -mtp 5000 \
		-t aym bzd cni gn hch nah oto quy shp tar -s es --spm $< > $@ &

## download models from zenodod
modelB-100dev-170k.pt sp-12lang-32k.spm:
	wget -O $@ ${ZENODO_HOME}/$@?download=1

## install OpenNMT-py and clone the git repo
OpenNMT-py:
	sudo pip install OpenNMT-py
	git clone https://github.com/OpenNMT/OpenNMT-py.git



## for the AmericasNLP 2023 model:

## start the OpenNMT-py server
americasnlp2023-onmt.log: americasnlp2023.json OpenNMT-py model_ml_step_194000.pt
	nohup python3 OpenNMT-py/server.py --port 5010 -c $< >> $@ &

## start the OPUS-MT wrapper
americasnlp2023-opusMT.log: all_32k.model
	nohup python3 opusMT-onmt-server2023.py -p 5011 -mtp 5010 \
		-t aym bzd cni czn gn hch nah oto quy shp tar -s es --spm $< > $@ &
