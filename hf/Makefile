#-*-makefile-*-
#
# recipes for converting OPUS-MT models to pyTorch/huggingface
# and for uploading them to the huggingface model hub
#
## TODO: does this work?
## 
## * vocabularies in SPM files (joint or separate vocabs): e.g
## 	eng-fin/opusTCv20210807+nopar+ft95-jointvoc_transformer-tiny11-align_2022-01-27.zip
##	eng-fin/opusTCv20210807+nopar+ft95-sepvoc_transformer-tiny11-align_2022-01-25.zip
##   --> create yaml-files on the fly for the joint vocab file? (from *.vocab file?)
##   --> different conversion script for separate vocab files?
##


## list all models that need to be converted
##   TODO: find a good way to automatically select reasonable models
##   TODO: some kind of quality control before converting/publishing


# MARIAN_MODEL_URLS =
#	https://object.pouta.csc.fi/Tatoeba-MT-models/eng-hun/opusTCv20210807+bt_transformer-big_2022-02-25.zip
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/eng-hun/opus+bt-2021-04-13.zip 
#	https://object.pouta.csc.fi/Tatoeba-MT-models/eng-hun/opusTCv20210807+bt_transformer-big_2022-02-25.zip
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/gmw-gmw/opus-2021-02-23.zip \
#	https://object.pouta.csc.fi/Tatoeba-MT-models/eng-fin/opusTCv20210807+bt-2021-09-01.zip
#	https://object.pouta.csc.fi/Tatoeba-MT-models/eng-fin/opusTCv20210807+bt-2021-12-08.zip \
#	https://object.pouta.csc.fi/Tatoeba-MT-models/eng-fin/opusTCv20210807+bt-2021-09-01.zip \
#	https://object.pouta.csc.fi/Tatoeba-MT-models/gmw-eng/opus4m+btTCv20210807-2021-09-30.zip

## broken yml file:
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/eng-gmw/opus1m+bt-2021-04-10.zip


## models for Ukrainian

# 	https://object.pouta.csc.fi/Tatoeba-MT-models/fin-eng/opusTCv20210807+bt-2021-12-08.zip \
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/eng-fin/opusTCv20210807+bt_transformer-big_2022-03-09.zip
# 	https://object.pouta.csc.fi/Tatoeba-MT-models/zle-eng/opusTCv20210807+bt_transformer-big_2022-03-17.zip \
#	https://object.pouta.csc.fi/Tatoeba-MT-models/eng-zle/opusTCv20210807+bt_transformer-big_2022-03-13.zip


# done for Ukrainian (2022-03-23)

# https://object.pouta.csc.fi/Tatoeba-MT-models/ukr-fin/opusTCv20210807+pft+pbt_transformer-align_2022-03-17.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/ukr-ces+slk/opusTCv20210807+pft_transformer-align_2022-03-17.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/ukr-hun/opusTCv20210807+pft_transformer-align_2022-03-08.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/ukr-ron/opusTCv20210807+pft_transformer-align_2022-03-08.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/ukr-tur/opusTCv20210807+pft_transformer-align_2022-03-07.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-bat/opusTCv20210807_transformer-align_2022-03-14.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-deu/opusTCv20210807_transformer-big_2022-03-19.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-eng/opusTCv20210807+bt_transformer-big_2022-03-17.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-fra/opusTCv20210807_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-gmq/opusTCv20210807+pft_transformer-big_2022-03-14.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-ita/opusTCv20210807_transformer-big_2022-03-19.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-por/opusTCv20210807_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-spa/opusTCv20210807_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-zle/opusTCv20210807+bt_transformer-big_2022-03-07.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-zls/opusTCv20210807+bt_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-zlw/opusTCv20210807+bt_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/bat-zle/opusTCv20210807_transformer-align_2022-03-13.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/ces+slk-ukr/opusTCv20210807+pbt_transformer-align_2022-03-08.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/deu-zle/opusTCv20210807_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/eng-zle/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/fin-ukr/opusTCv20210807+pbt_transformer-align_2022-03-07.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/fra-zle/opusTCv20210807_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/gmq-zle/opusTCv20210807+pbt_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/hun-ukr/opusTCv20210807+pbt_transformer-align_2022-03-08.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/ita-zle/opusTCv20210807_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/por-zle/opusTCv20210807_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/ron-ukr/opusTCv20210807+pbt_transformer-align_2022-03-08.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/spa-zle/opusTCv20210807_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/tur-ukr/opusTCv20210807+pbt_transformer-align_2022-03-07.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zls-zle/opusTCv20210807+bt_transformer-big_2022-03-23.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zlw-zle/opusTCv20210807+bt_transformer-big_2022-03-19.zip


## done for English-xxx both directions (big transformer)

# https://object.pouta.csc.fi/Tatoeba-MT-models/eng-fin/opusTCv20210807+bt_transformer-big_2022-03-09.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/zle-eng/opusTCv20210807+bt_transformer-big_2022-03-17.zip \
# https://object.pouta.csc.fi/Tatoeba-MT-models/eng-zle/opusTCv20210807+bt_transformer-big_2022-03-13.zip \

MARIAN_MODEL_URLS = \
https://object.pouta.csc.fi/Tatoeba-MT-models/eng-ara/opusTCv20210807+bt_transformer-big_2022-02-25.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/eng-bul/opusTCv20210807+bt_transformer-big_2022-02-25.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/eng-cat+oci+spa/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/eng-ces+slk/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/eng-ell/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/eng-est/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/eng-fra/opusTCv20210807+bt_transformer-big_2022-03-09.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/eng-gmq/opusTCv20210807+bt_transformer-big_2022-03-17.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/eng-hun/opusTCv20210807+bt_transformer-big_2022-02-25.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/eng-ita/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/eng-lav/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/eng-lit/opusTCv20210807+bt_transformer-big_2022-02-25.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/eng-por/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/eng-ron/opusTCv20210807+bt_transformer-big_2022-02-25.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/eng-spa/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/eng-tur/opusTCv20210807+bt_transformer-big_2022-02-25.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/ara-eng/opusTCv20210807+bt_transformer-big_2022-03-09.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/bul-eng/opusTCv20210807+bt_transformer-big_2022-03-09.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/cat+oci+spa-eng/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/cel-eng/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/ces+slk-eng/opusTCv20210807+bt_transformer-big_2022-03-17.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/ell-eng/opusTCv20210807+bt_transformer-big_2022-02-25.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/est-eng/opusTCv20210807+bt_transformer-big_2022-03-09.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/fra-eng/opusTCv20210807+bt_transformer-big_2022-03-09.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/gmq-eng/opusTCv20210807+bt_transformer-big_2022-03-09.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/hbs-eng/opusTCv20210807+bt_transformer-big_2022-02-25.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/heb-eng/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/hun-eng/opusTCv20210807+bt_transformer-big_2022-03-09.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/ita-eng/opusTCv20210807+bt_transformer-big_2022-02-25.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/lav-eng/opusTCv20210807+bt_transformer-big_2022-03-13.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/lit-eng/opusTCv20210807+bt_transformer-big_2022-02-25.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/tur-eng/opusTCv20210807+bt_transformer-big_2022-03-17.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/zls-eng/opusTCv20210807+bt_transformer-big_2022-03-17.zip \
https://object.pouta.csc.fi/Tatoeba-MT-models/zlw-eng/opusTCv20210807+bt_transformer-big_2022-03-17.zip


SHELL := bash

MARIAN_MODEL_URL ?= ${firstword ${MARIAN_MODEL_URLS}}

## extract language pair and release data from the URL
LANGPAIR     = $(notdir ${patsubst %/,%,${dir ${MARIAN_MODEL_URL}}})
RELEASE_DATE = ${shell echo '${basename ${MARIAN_MODEL_URL}}' | rev | cut -f1-3 -d\- | cut -f1 -d_ | rev}

## get language names and IDs in various variants
SRCLANGID   := $(firstword $(subst -, ,${LANGPAIR}))
TRGLANGID   := $(lastword $(subst -, ,${LANGPAIR}))
SRCLANG     := $(shell iso639 ${SRCLANGID} | tr '"' ' ' | xargs)
TRGLANG     := $(shell iso639 ${TRGLANGID} | tr '"' ' ' | xargs)

## two-letter codes
LANGPAIR2   := $(shell iso639 -2 -k -p ${LANGPAIR})
SRCLANGID2  := $(firstword $(subst -, ,${LANGPAIR2}))
TRGLANGID2  := $(lastword $(subst -, ,${LANGPAIR2}))

## three-letter codes
LANGPAIR3   := $(shell iso639 -3 -k -p ${LANGPAIR})
SRCLANGID3  := $(firstword $(subst -, ,${LANGPAIR3}))
TRGLANGID3  := $(lastword $(subst -, ,${LANGPAIR3}))

## the name of the workdir with the original MarianNMT model
MARIAN_MODEL     := marian-models/${basename ${notdir ${MARIAN_MODEL_URL}}}/${LANGPAIR2}

ifneq (${wildcard ${MARIAN_MODEL}/README.md},)
  MODEL_TYPE = ${shell grep 'model:' ${MARIAN_MODEL}/README.md | head -1 | cut -f2 -d: | xargs}
  MODEL_DATA = ${shell grep 'dataset:' ${MARIAN_MODEL}/README.md | head -1 | cut -f2 -d: | xargs}
  MODEL_PRE = ${shell grep 'pre-processing:' ${MARIAN_MODEL}/README.md | head -1 | cut -f2 -d: | xargs}
  MODEL_TOK = ${filter-out normalization +,${MODEL_PRE}}
  MODEL_SRCVOCAB = ${shell grep -A2 'vocabs:' ${MARIAN_MODEL}/decoder.yml | tail -2 | head -1 | sed 's/^ *\- *//' | xargs}
  MODEL_TRGVOCAB = ${shell grep -A2 'vocabs:' ${MARIAN_MODEL}/decoder.yml | tail -1 | sed 's/^ *\- *//' | xargs}
  MODEL_SRCSPM    = ${MARIAN_MODEL}/source.spm
  MODEL_TRGSPM    = ${MARIAN_MODEL}/target.spm
  MODEL_SRCLANGS  = ${shell perl extract_reasonable_languages.pl ${MARIAN_MODEL}/README.md | head -1}
  MODEL_TRGLANGS  = ${shell perl extract_reasonable_languages.pl ${MARIAN_MODEL}/README.md | head -2 | tail -1}
#  MODEL_SRCLANGS  = ${shell grep 'source language(s):' ${MARIAN_MODEL}/README.md | head -1 | cut -f2 -d: | xargs}
#  MODEL_TRGLANGS  = ${shell grep 'target language(s):' ${MARIAN_MODEL}/README.md | head -1 | cut -f2 -d: | xargs}
  MODEL_TRGLABELS = $(sort ${shell grep 'valid language labels:' ${MARIAN_MODEL}/README.md | head -1 | cut -f2 -d: | xargs})
  MODEL_LANGIDS2  = ${shell iso639 -2 -k ${sort ${MODEL_SRCLANGS} ${MODEL_TRGLANGS}}}
  MODEL_VOCAB_TXT = ${wildcard ${MARIAN_MODEL}/*.vocab}
  MODEL_VOCAB_YML = ${patsubst %,%.yml,${MODEL_VOCAB_TXT}}
endif

# ## replace target languages with the ones that are actually supported!
# ifneq (${MODEL_TRGLABELS},)
#   USE_LABELS = 1
#   MODEL_TRGLANGS = $(subst >>,,$(subst <<,,${MODEL_TRGLABELS}))
# endif

## multiple target languages always require labels
ifeq (${MODEL_TRGLABELS},)
ifneq ($(words ${MODEL_TRGLANGS}),1)
  USE_LABELS = 1
  MODEL_TRGLABELS = ${patsubst %,>>%<<,${MODEL_TRGLANGS}}
endif
else
  USE_LABELS = 1
endif


BACKGROUND_READING = [OPUS-MT – Building open translation services for the World](https://aclanthology.org/2020.eamt-1.61/)

## base name for huggingface
## tc = trained on tatoeba challenge data
ifeq ($(findstring Tatoeba-MT-models,${MARIAN_MODEL_URL}),)
  HF_BASENAME   = opus-mt
  DATA_SOURCE   = https://opus.nlpl.eu/
  OPUSMT_README = https://github.com/Helsinki-NLP/OPUS-MT-train/tree/master/models/${LANGPAIR}/README.md
else
  HF_BASENAME = opus-mt-tc
  DATA_SOURCE = https://github.com/Helsinki-NLP/Tatoeba-Challenge
  OPUSMT_README = https://github.com/Helsinki-NLP/Tatoeba-Challenge/tree/master/models/${LANGPAIR}/README.md
  BACKGROUND_READING += and [The Tatoeba Translation Challenge – Realistic Data Sets for Low Resource and Multilingual MT](https://aclanthology.org/2020.wmt-1.139/)
endif

## modeltype to be marked in the name
## set to base if no extension to "transformer" is given
HF_MODELTYPE = $(subst transformer-,,$(subst -align,,${MODEL_TYPE}))
ifeq (${HF_MODELTYPE},transformer)
  HF_MODELTYPE = base
endif


HF_NAME       := ${subst +,_,${HF_BASENAME}-${HF_MODELTYPE}-${LANGPAIR2}}
PYTORCH_MODEL := pytorch-models/${HF_NAME}

.PHONY: all
all:
	@for m in ${MARIAN_MODEL_URLS}; do \
	  ${MAKE} MARIAN_MODEL_URL=$$m process; \
	done


.PHONY: convert-all
convert-all:
	@for m in ${MARIAN_MODEL_URLS}; do \
	  ${MAKE} MARIAN_MODEL_URL=$$m fetch-and-convert; \
	done

.PHONY: commit-all
commit-all:
	@for m in ${MARIAN_MODEL_URLS}; do \
	  ${MAKE} MARIAN_MODEL_URL=$$m commit; \
	done

.PHONY: fetch-and-convert
fetch-and-convert:
	${MAKE} fetch
	${MAKE} convert

.PHONY: process
process:
	${MAKE} fetch
	${MAKE} convert
	${MAKE} commit

.PHONY: info
info:
	@echo "workdir: ${MARIAN_MODEL}"
	@echo "release: ${RELEASE_DATE}"
	@echo "langpair: ${LANGPAIR} (${SRCLANGID3},${TRGLANGID3}) (${SRCLANGID2},${TRGLANGID2}) (${SRCLANG},${TRGLANG})"
	@echo "type: ${MODEL_TYPE}"
	@echo "data: ${MODEL_DATA}"
	@echo "tokenization: ${MODEL_TOK}"
	@echo "vocab: ${sort ${MODEL_SRCVOCAB} ${MODEL_SRCVOCAB}}"
	@echo "source langs: ${MODEL_SRCLANGS}"
	@echo "target langs: ${MODEL_TRGLANGS}"
	@echo "hfname: ${HF_NAME}"
	@echo
	@echo "testset file: ${TESTSET_TRANSLATIONS_FILE}"

.PHONY: fetch
fetch: ${MARIAN_MODEL}

.PHONY: convert
convert: ${PYTORCH_MODEL}/README.md

.PHONY: commit
commit: ${PYTORCH_MODEL}.committed


## in case we need to convert vocab files to yaml
.PHONY: vocabs
vocabs: ${MODEL_VOCAB_YML}

${MODEL_VOCAB_YML}: %.yml: %
	./vocab2yaml.py < $< > $@


## huggingface access token

${HOME}/.huggingface/token:
	huggingface-cli login
	git config --global credential.helper store


## create the repository item and upload the model

ifneq (${HF_NAME},)
${PYTORCH_MODEL}.committed: ${PYTORCH_MODEL} ${PYTORCH_MODEL}/README.md ${HOME}/.huggingface/token
	-huggingface-cli repo create ${HF_NAME} --organization Helsinki-NLP --yes
	-git clone https://tiedeman:`cat ${HOME}/.huggingface/token`@huggingface.co/Helsinki-NLP/${HF_NAME}
	cd ${HF_NAME} && git lfs install
	cd ${HF_NAME} && git lfs track "*.spm"
	cd ${HF_NAME} && git config --global user.email "jorg.tiedemann@helsinki.fi"
	cd ${HF_NAME} && git config --global user.name "Joerg Tiedemann"
	mv ${PYTORCH_MODEL}/* ${HF_NAME}/
	rsync ${HF_NAME}/README.md ${PYTORCH_MODEL}/README.md
	cd ${HF_NAME} && git add .
	cd ${HF_NAME} && git commit -m "Initial commit"
	cd ${HF_NAME} && git push
	touch $@
endif



# fetch the original MarianNMT model

${MARIAN_MODEL}:
	mkdir -p $@
	wget -O $@/model.zip ${MARIAN_MODEL_URL}
	cd $@ && unzip model.zip
	rm -f $@/model.zip


transformers:
	git clone https://github.com/huggingface/transformers.git
	cd transformers
	pip install -e .

# convert the model to pyTorch

${PYTORCH_MODEL}: ${MARIAN_MODEL} ${MODEL_VOCAB_YML} transformers
	export PYTHONPATH=transformers/src:${PYTHONPATH} && \
	python convert_to_pytorch.py --model-path $< --dest-path $@

#	export PYTHONPATH=${HOME}/research/Tatoeba-Challenge/transformers/src:${PYTHONPATH} && \
#	python3 convert_to_pytorch.py --model-path $< --dest-path $@



## files with benchmarks and test set translations

ifneq (${wildcard ${MARIAN_MODEL}/README.md},)
  TESTSET_TRANSLATIONS_FILE = ${shell grep 'test set translations:' ${MARIAN_MODEL}/README.md | cut -f2 -d'(' | sed 's/)$$//'}
  TESTSET_OUTPUT_FILE = ${shell grep 'test set scores:' ${MARIAN_MODEL}/README.md | cut -f2 -d'(' | sed 's/)$$//'}
endif

SCORES_FILE = ${MARIAN_MODEL_URL:.zip=.scores.txt}
EVAL_FILE = ${MARIAN_MODEL_URL:.zip=.eval.zip}


${PYTORCH_MODEL}/benchmark_results.txt:
	-wget -q -O - ${SCORES_FILE} | cut -f1-4,6,7 > $@
	if [ ! -s $@ ]; then \
	  grep '^|' ${MARIAN_MODEL}/README.md | \
	  tail -n +3  | tr "\t" ' ' | tr '|' "\t" | sed 's/ //g' | cut -f2- | \
	  sed 's/^\([^	]*\)\.\([^	]*\)	/\2	\1	/' |\
	  awk '{ t = $$4; $$4 = $$3; $$3 = t; print } ' FS='\t' OFS='\t' |\
	  sed 's/Tatoeba-test/tatoeba-test-v2020-07-28/' |\
	  cut -f1-6 > $@; \
	fi

${PYTORCH_MODEL}/benchmark_translations.zip:
	-wget -q -O $@ ${EVAL_FILE}
	if [ ! -e $@ ]; then \
	  wget -q -O ${dir $@}${notdir ${TESTSET_OUTPUT_FILE}} ${TESTSET_OUTPUT_FILE}; \
	  cd ${dir $@}; zip $@ ${notdir ${TESTSET_OUTPUT_FILE}}; \
	  rm -f ${notdir ${TESTSET_OUTPUT_FILE}}; \
	fi

## verify that there is something in the test set translations
## get an example and example output
## use dummy string if no example can be downloaded

ifdef TESTSET_TRANSLATIONS_FILE
ifeq (${shell wget -q -O - ${TESTSET_TRANSLATIONS_FILE} | head -3 | wc -l | xargs},3)
  TESTSET_INPUT_EXAMPLE   := ${subst ",\",${shell wget -q -O - ${TESTSET_TRANSLATIONS_FILE} | head -1}}
  TESTSET_OUTPUT_EXAMPLE  := ${subst ",\",${shell wget -q -O - ${TESTSET_TRANSLATIONS_FILE} | head -3 | tail -1}}
  TESTSET_INPUT2_EXAMPLE  := ${subst ",\",${shell wget -q -O - ${TESTSET_TRANSLATIONS_FILE} | tail -4 | head -1}}
  TESTSET_OUTPUT2_EXAMPLE := ${subst ",\",${shell wget -q -O - ${TESTSET_TRANSLATIONS_FILE} | tail -2 | head -1}}
#  TESTSET_INPUT2_EXAMPLE = ${shell wget -q -O - ${TESTSET_TRANSLATIONS_FILE} | head -5 | tail -1}
#  TESTSET_OUTPUT2_EXAMPLE = ${shell wget -q -O - ${TESTSET_TRANSLATIONS_FILE} | head -7 | tail -1}
else
ifeq (${USE_LABELS},1)
  TESTSET_INPUT_EXAMPLE  := ${firstword ${MODEL_TRGLABELS}} Replace this with text in an accepted source language.
  TESTSET_INPUT2_EXAMPLE := ${lastword ${MODEL_TRGLABELS}} This is the second sentence.
else
  TESTSET_INPUT_EXAMPLE  := Replace this with text in an accepted source language.
  TESTSET_INPUT2_EXAMPLE := This is the second sentence.
endif
endif
endif

## create the model card

${PYTORCH_MODEL}/README.md: ${PYTORCH_MODEL} ${PYTORCH_MODEL}/benchmark_results.txt ${PYTORCH_MODEL}/benchmark_translations.zip
	@echo "..... create $@"
	@echo '---'                 > $@
	@echo 'language:'          >> $@
	@for l in ${sort ${SRCLANGID2} ${TRGLANGID2} ${MODEL_LANGIDS2}}; do \
	  echo "- $$l"             >> $@; \
	done
#	@echo '- ${SRCLANGID2}'    >> $@
#	@echo '- ${TRGLANGID2}'    >> $@
	@echo ''                   >> $@
	@echo 'tags:'              >> $@
	@echo '- translation'      >> $@
	@echo ''                   >> $@
	@echo 'license: cc-by-4.0' >> $@
	@echo 'model-index:'       >> $@
	@echo '- name: ${HF_NAME}' >> $@
	@echo '  results:'         >> $@
	./extract-task-results.pl ${PYTORCH_MODEL}/benchmark_results.txt >> $@
	@echo '---'                >> $@
	@echo '# ${HF_NAME}'       >> $@
	@echo ''                   >> $@
	@echo 'Neural machine translation model for translating from ${SRCLANG} (${SRCLANGID2}) to ${TRGLANG} (${TRGLANGID2}).' >> $@
	@echo ''                   >> $@
	@echo 'This model is part of the [OPUS-MT project](https://github.com/Helsinki-NLP/Opus-MT), an effort to make neural machine translation models widely available and accessible for many languages in the world. All models are originally trained using the amazing framework of [Marian NMT](https://marian-nmt.github.io/), an efficient NMT implementation written in pure C++. The models have been converted to pyTorch using the transformers library by huggingface. Training data is taken from [OPUS](https://opus.nlpl.eu/) and training pipelines use the procedures of [OPUS-MT-train](https://github.com/Helsinki-NLP/Opus-MT-train).' >> $@
	@echo ''                                                        >> $@
	@echo '* Publications: ${BACKGROUND_READING} (Please, cite if you use this model.)' >> $@
	@echo ''                                                        >> $@
	@echo '```'                                                     >> $@
	@echo '@inproceedings{tiedemann-thottingal-2020-opus,'          >> $@
	@echo '    title = "{OPUS}-{MT} {--} Building open translation services for the World",' >> $@
	@echo '    author = {Tiedemann, J{\"o}rg  and Thottingal, Santhosh},' >> $@
	@echo '    booktitle = "Proceedings of the 22nd Annual Conference of the European Association for Machine Translation",' >> $@
	@echo '    month = nov,'                                        >> $@
	@echo '    year = "2020",'                                      >> $@
	@echo '    address = "Lisboa, Portugal",'                       >> $@
	@echo '    publisher = "European Association for Machine Translation",' >> $@
	@echo '    url = "https://aclanthology.org/2020.eamt-1.61",'    >> $@
	@echo '    pages = "479--480",'                                 >> $@
	@echo '}'                                                       >> $@
ifeq (${HF_BASENAME},opus-mt-tc)
	@echo ''                                                        >> $@
	@echo '@inproceedings{tiedemann-2020-tatoeba,'                  >> $@
	@echo '    title = "The Tatoeba Translation Challenge {--} Realistic Data Sets for Low Resource and Multilingual {MT}",' >> $@
	@echo '    author = {Tiedemann, J{\"o}rg},'                     >> $@
	@echo '    booktitle = "Proceedings of the Fifth Conference on Machine Translation",' >> $@
	@echo '    month = nov,'                                        >> $@
	@echo '    year = "2020",'                                      >> $@
	@echo '    address = "Online",'                                 >> $@
	@echo '    publisher = "Association for Computational Linguistics",' >> $@
	@echo '    url = "https://aclanthology.org/2020.wmt-1.139",'    >> $@
	@echo '    pages = "1174--1182",'                               >> $@
	@echo '}'                                                       >> $@
endif
	@echo '```'                                                     >> $@
	@echo ''                                                        >> $@
	@echo '## Model info'                                           >> $@
	@echo ''                                                        >> $@
	@echo '* Release: ${RELEASE_DATE}'                              >> $@
	@echo '* source language(s): ${MODEL_SRCLANGS}'                 >> $@
	@echo '* target language(s): ${MODEL_TRGLANGS}'                 >> $@
ifeq (${USE_LABELS},1)
	@echo '* valid target language labels: ${MODEL_TRGLABELS}'      >> $@
endif
#	@echo '* model: ${MODEL_TYPE} (${HF_MODELTYPE})'                >> $@
	@echo '* model: ${MODEL_TYPE}'                                  >> $@
	@echo '* data: ${MODEL_DATA} ([source](${DATA_SOURCE}))'        >> $@
	@echo '* tokenization: ${MODEL_TOK}'                            >> $@
	@echo '* original model: [$(notdir ${MARIAN_MODEL_URL})](${MARIAN_MODEL_URL})' >> $@
	@echo '* more information released models: [OPUS-MT ${LANGPAIR} README](${OPUSMT_README})'     >> $@
ifeq (${USE_LABELS},1)
	@echo "* more information about the model: [MarianMT](https://huggingface.co/docs/transformers/model_doc/marian)" >>$@
	@echo ''                                                        >> $@
	@echo 'This is a multilingual translation model with multiple target languages. A sentence initial language token is required in the form of `>>id<<` (id = valid target language ID), e.g. `>>${firstword ${MODEL_TRGLANGS}}<<`' >> $@
endif
	@echo ''                                                        >> $@
	@echo '## Usage'                                                >> $@
	@echo ''                                                        >> $@
	@echo 'A short example code:'                                   >> $@
	@echo ''                                                        >> $@
	@echo '```python'                                               >> $@
	@echo 'from transformers import MarianMTModel, MarianTokenizer' >> $@
	@echo ''                                                        >> $@
	@echo 'src_text = ['                                            >> $@
	@echo "    \"${TESTSET_INPUT_EXAMPLE}\","                       >> $@
	@echo "    \"${TESTSET_INPUT2_EXAMPLE}\""                       >> $@
	@echo ']'                                                       >> $@
	@echo ''                                                        >> $@
	@echo 'model_name = "pytorch-models/${HF_NAME}"'     >> $@
	@echo 'tokenizer = MarianTokenizer.from_pretrained(model_name)' >> $@
	@echo 'model = MarianMTModel.from_pretrained(model_name)'       >> $@
	@echo 'translated = model.generate(**tokenizer(src_text, return_tensors="pt", padding=True))' >> $@
	@echo ''                                                        >> $@
	@echo 'for t in translated:'                                    >> $@
	@echo '    print( tokenizer.decode(t, skip_special_tokens=True) )' >> $@
ifdef TESTSET_OUTPUT_EXAMPLE
	@echo ''                                                        >> $@
	@echo '# expected output:'                                      >> $@
	@echo "#     ${TESTSET_OUTPUT_EXAMPLE}"                         >> $@
	@echo "#     ${TESTSET_OUTPUT2_EXAMPLE}"                        >> $@
endif
	@echo '```'                                                     >> $@
	@echo ''                                                        >> $@
	@echo 'You can also use OPUS-MT models with the transformers pipelines, for example:' >> $@
	@echo ''                                                        >> $@
	@echo '```python'                                               >> $@
	@echo 'from transformers import pipeline'                       >> $@
	@echo 'pipe = pipeline("translation", model="Helsinki-NLP/${HF_NAME}")' >> $@
	@echo "print(pipe(\"${TESTSET_INPUT_EXAMPLE}\"))"               >> $@
ifdef TESTSET_OUTPUT_EXAMPLE
	@echo ''                                                        >> $@
	@echo "# expected output: ${TESTSET_OUTPUT_EXAMPLE}"            >> $@
endif
	@echo '```'                                                     >> $@
	@echo ''                                                        >> $@
	@echo '## Benchmarks'                                           >> $@
	@echo ''                                                        >> $@
	@grep 'test set translations:' ${MARIAN_MODEL}/README.md        >> $@
	@grep 'test set scores:' ${MARIAN_MODEL}/README.md              >> $@
	@echo '* benchmark results: [benchmark_results.txt](benchmark_results.txt)' >> $@
	@echo '* benchmark output: [benchmark_translations.zip](benchmark_translations.zip)' >> $@
	@echo ''                                                        >> $@
	@echo '| langpair | testset | chr-F | BLEU  | #sent | #words |' >> $@
	@echo '|----------|---------|-------|-------|-------|--------|' >> $@
	t=`cut -f2 < ${PYTORCH_MODEL}/benchmark_results.txt | grep tatoeba | sort -u | tail -1`; \
	if [ "$$t" != "" ]; then \
	  grep "$$t" ${PYTORCH_MODEL}/benchmark_results.txt |\
	  awk '{if (($$3 > 0.4 || $$4 > 20) && $$5 > 199) print}' |\
	  sed 's/	/ | /g;s/^/| /;s/$$/ |/'                        >> $@; \
	fi
	@cat ${PYTORCH_MODEL}/benchmark_results.txt | \
	grep -v 'flores101-dev	' | grep -v 'tatoeba-test' |\
	awk '{if (($$3 > 0.4 || $$4 > 20) && $$5 > 199) print}' |\
	sed 's/	/ | /g;s/^/| /;s/$$/ |/'                                >> $@
	@echo ''                                                        >> $@
	@echo '## Acknowledgements'                                     >> $@
	@echo ''                                                        >> $@
	@echo 'The work is supported by the [European Language Grid](https://www.european-language-grid.eu/) as [pilot project 2866](https://live.european-language-grid.eu/catalogue/#/resource/projects/2866), by the [FoTran project](https://www.helsinki.fi/en/researchgroups/natural-language-understanding-with-cross-lingual-grounding), funded by the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation programme (grant agreement No 771113), and the [MeMAD project](https://memad.eu/), funded by the European Union’s Horizon 2020 Research and Innovation Programme under grant agreement No 780069. We are also grateful for the generous computational resources and IT infrastructure provided by [CSC -- IT Center for Science](https://www.csc.fi/), Finland.' >> $@
	@echo ''                                                        >> $@
	@echo '## Model conversion info'                                >> $@
	@echo ''                                                        >> $@
	@echo '* transformers version: ${shell echo "import transformers#print(transformers.__version__)" | tr '#' "\n" | python3}' >> $@
	@echo '* OPUS-MT git hash: ${shell git rev-parse --short HEAD}' >> $@
	@echo '* port time: ${shell date}'                              >> $@
	@echo '* port machine: ${shell hostname}'                       >> $@





## OLD: extract benchmark scores

# ifeq (${shell wget -q -O - ${SCORES_FILE} | head -3 | wc -l | xargs},3)
#	@echo '* additional benchmark results: [${notdir ${SCORES_FILE}}](${SCORES_FILE})' >> $@
#	@echo '* additional benchmark output: [${notdir ${EVAL_FILE}}](${EVAL_FILE})'      >> $@
# 	@echo ''                                                        >> $@
# 	@echo '| langpair | testset | chr-F | BLEU  | #sent | #words |' >> $@
# 	@echo '|----------|---------|-------|-------|-------|--------|' >> $@
# 	@wget -q -O - ${SCORES_FILE} |\
# 	cut -f1-4,6,7 | \
# 	awk '{if (($$3 > 0.4 || $$4 > 20) && $$5 > 199) print}' |\
# 	sed 's/	/ | /g;s/^/| /;s/$$/ |/'                                >> $@
# else
# 	@echo ''                                                        >> $@
# 	@perl extract_reasonable_languages.pl ${MARIAN_MODEL}/README.md | grep '^|' >> $@
# endif
