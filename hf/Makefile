
## TODO:
## 
## * mark different model types (transformer big/base/small/tiny), e.g. big:
##	https://object.pouta.csc.fi/Tatoeba-MT-models/fin-eng/opusTCv20210807+bt-2021-12-08.zip
## * vocabularies in SPM files (joint vocabs): e.g
## 	eng-fin/opusTCv20210807+nopar+ft95-jointvoc_transformer-tiny11-align_2022-01-27.zip
## * vocabularies in SPM files (separate vocabs): e.g
##	eng-fin/opusTCv20210807+nopar+ft95-sepvoc_transformer-tiny11-align_2022-01-25.zip
##


## list all models that need to be converted
##   TODO: find a good way to automatically select reasonable models
##   TODO: some kind of quality control before converting/publishing
##   IDEA: only list languages that have reasonable scores?

MARIAN_MODEL_URLS = https://object.pouta.csc.fi/Tatoeba-MT-models/gmw-gmw/opus-2021-02-23.zip \
		https://object.pouta.csc.fi/Tatoeba-MT-models/eng-fin/opusTCv20210807+bt-2021-09-01.zip \
		https://object.pouta.csc.fi/Tatoeba-MT-models/gmw-eng/opus4m+btTCv20210807-2021-09-30.zip

## broken yml file:
# https://object.pouta.csc.fi/Tatoeba-MT-models/eng-gmw/opus1m+bt-2021-04-10.zip


MARIAN_MODEL_URL ?= ${firstword ${MARIAN_MODEL_URLS}}

## extract language pair and release data from the URL
LANGPAIR     = $(notdir ${patsubst %/,%,${dir ${MARIAN_MODEL_URL}}})
RELEASE_DATE = ${shell echo '${basename ${MARIAN_MODEL_URL}}' | rev | cut -f1-3 -d\- | rev}

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
endif

# ## replace target languages with the ones that are actually supported!
# ifneq (${MODEL_TRGLABELS},)
#   USE_LABELS = 1
#   MODEL_TRGLANGS = $(subst >>,,$(subst <<,,${MODEL_TRGLABELS}))
# endif

## multiple target languages always require labels
ifeq (${MODEL_TRGLABELS},)
ifneq ($(words ${MODEL_TRGLABELS}),1)
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


HF_NAME       := ${HF_BASENAME}-${HF_MODELTYPE}-${LANGPAIR2}
PYTORCH_MODEL := pytorch-models/${HF_NAME}

all:
	@for m in ${MARIAN_MODEL_URLS}; do \
	  ${MAKE} MARIAN_MODEL_URL=$$m fetch; \
	  ${MAKE} MARIAN_MODEL_URL=$$m convert; \
	  ${MAKE} MARIAN_MODEL_URL=$$m commit; \
	done

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

.PHONY: fetch
fetch: ${MARIAN_MODEL}

.PHONY: convert
convert: ${PYTORCH_MODEL}/README.md

.PHONY: commit
commit: ${PYTORCH_MODEL}.committed



## huggingface access token

${HOME}/.huggingface/token:
	huggingface-cli login
	git config --global credential.helper store


## create the repository item and upload the model

ifneq (${HF_NAME},)
${PYTORCH_MODEL}.committed: ${PYTORCH_MODEL} ${PYTORCH_MODEL}/README.md ${HOME}/.huggingface/token
	-huggingface-cli repo create ${HF_NAME} --organization Helsinki-NLP
	-git clone https://tiedeman:`cat ${HOME}/.huggingface/token`@huggingface.co/Helsinki-NLP/${HF_NAME}
	cd ${HF_NAME} && git lfs install
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


# convert the model to pyTorch

${PYTORCH_MODEL}: ${MARIAN_MODEL}
	python3 convert_to_pytorch.py --model-path $< --dest-path $@


## create the model card

${PYTORCH_MODEL}/README.md: ${PYTORCH_MODEL}
	@echo "..... create $@"
	@echo '---'                 > $@
	@echo 'language:'          >> $@
	@echo '- ${SRCLANGID2}'    >> $@
	@echo '- ${TRGLANGID2}'    >> $@
	@echo ''                   >> $@
	@echo 'tags:'              >> $@
	@echo '- translation'      >> $@
	@echo ''                   >> $@
	@echo 'license: cc-by-4.0' >> $@
	@echo '---'                >> $@
	@echo '# ${HF_NAME}'       >> $@
	@echo ''                   >> $@
	@echo 'Neural machine translation model for translating from ${SRCLANG} (${SRCLANGID2}) to ${TRGLANG} (${TRGLANGID2}).' >> $@
	@echo ''                   >> $@
	@echo 'This model is part of the [OPUS-MT project](https://github.com/Helsinki-NLP/Opus-MT), an effort to make neural machine translation models widely available and accessible for many languages in the world. All models are originally trained using the amazing framework of [Marian NMT](https://marian-nmt.github.io/), an efficient NMT implementation written in pure C++. The models have been converted to pyTorch using the transformers library by huggingface. Training data is taken from [OPUS](https://opus.nlpl.eu/) and training pipelines use the procedures of [OPUS-MT-train](https://github.com/Helsinki-NLP/Opus-MT-train).' >> $@
	@echo ''                     >> $@
	@echo '* Publications: ${BACKGROUND_READING} (Please, cite if you use this model.)' >> $@
	@echo ''                     >> $@
	@echo '## Model info'        >> $@
	@echo ''                     >> $@
	@echo '* Release: ${RELEASE_DATE}' >> $@
	@echo '* source language(s): ${MODEL_SRCLANGS}'  >> $@
	@echo '* target language(s): ${MODEL_TRGLANGS}'  >> $@
ifeq (${USE_LABELS},1)
	@echo '* valid target language labels: ${MODEL_TRGLABELS}'  >> $@
endif
	@echo '* model: ${MODEL_TYPE} (${HF_MODELTYPE})'            >> $@
	@echo '* data: ${MODEL_DATA} ([source](${DATA_SOURCE}))'    >> $@
	@echo '* tokenization: ${MODEL_TOK}'                        >> $@
	@echo '* original model: [$(notdir ${MARIAN_MODEL_URL})](${MARIAN_MODEL_URL})' >> $@
	@echo '* more information: [OPUS-MT ${LANGPAIR} README](${OPUSMT_README})'     >> $@
ifeq (${USE_LABELS},1)
	@echo ''                     >> $@
	@echo 'This is a multilingual translation model with multiple target languages. A sentence initial language token is required in the form of `>>id<<` (id = valid target language ID), e.g. `>>${firstword ${MODEL_TRGLANGS}}<<`' >> $@
endif
	@echo ''                     >> $@
	@echo '## Usage'             >> $@
	@echo ''                     >> $@
	@echo 'You can use OPUS-MT models with the transformers pipelines, for example:' >> $@
	@echo ''                     >> $@
	@echo '```python'            >> $@
	@echo 'from transformers import pipeline' >> $@
	@echo 'pipe = pipeline("translation", model="Helsinki-NLP/${HF_NAME}")' >> $@
ifeq (${USE_LABELS},1)
	@echo 'print(pipe("${firstword ${MODEL_TRGLABELS}} Replace this with text in an accepted source language."))' >> $@
else
	@echo 'print(pipe("Replace this with a sentence in an accepted source language.")' >> $@
endif
	@echo '```'                  >> $@
	@echo ''                     >> $@
	@echo '## Benchmarks'        >> $@
	@echo ''                     >> $@
	@grep 'test set translations:' ${MARIAN_MODEL}/README.md >> $@
	@grep 'test set scores:' ${MARIAN_MODEL}/README.md >> $@
	@echo ''                     >> $@
	@perl extract_reasonable_languages.pl ${MARIAN_MODEL}/README.md | grep '^|' >> $@
	@echo ''                     >> $@
	@echo '## Acknowledgements'  >> $@
	@echo ''                     >> $@
	@echo 'The work is supported by the [European Language Grid](https://www.european-language-grid.eu/) as [pilot project 2866](https://live.european-language-grid.eu/catalogue/#/resource/projects/2866), by the [FoTran project](https://www.helsinki.fi/en/researchgroups/natural-language-understanding-with-cross-lingual-grounding), funded by the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation programme (grant agreement No 771113), and the [MeMAD project](https://memad.eu/), funded by the European Union’s Horizon 2020 Research and Innovation Programme under grant agreement No 780069. We are also grateful for the generous computational resources and IT infrastructure provided by [CSC -- IT Center for Science](https://www.csc.fi/), Finland.' >> $@
	@echo ''                           >> $@
	@echo '## Model conversion info'   >> $@
	@echo ''                           >> $@
	@echo '* transformers version: ${shell echo "import transformers#print(transformers.__version__)" | tr '#' "\n" | python3}' >> $@
	@echo '* OPUS-MT git hash: ${shell git rev-parse --short HEAD}' >> $@
	@echo '* port time: ${shell date}'  >> $@
	@echo '* port machine: ${shell hostname}'  >> $@
