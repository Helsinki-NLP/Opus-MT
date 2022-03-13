



STORAGE_HOME = https://object.pouta.csc.fi
MODELS = 	Tatoeba-MT-models/gmw-eng/opus1m+bt-2021-05-01.zip \
		Tatoeba-MT-models/eng-gmw/opus1m+bt-2021-04-10.zip \
		Tatoeba-MT-models/eng-roa/opus1m+bt-2021-04-10.zip \
		Tatoeba-MT-models/roa-eng/opus1m+bt-2021-05-01.zip \
		Tatoeba-MT-models/eng-gmq/opus1m+bt-2021-04-13.zip \
		Tatoeba-MT-models/gmq-eng/opus1m+bt-2021-05-01.zip \
		Tatoeba-MT-models/zle-eng/opus1m+bt-2021-05-02.zip \
		Tatoeba-MT-models/eng-zle/opus1m+bt-2021-04-10.zip \
		Tatoeba-MT-models/eng-eus/opus+bt-2021-03-07.zip \
		Tatoeba-MT-models/eus-eng/opus+bt-2021-04-30.zip
# MODELS = 	Tatoeba-MT-models/gmw-eng/opus1m+bt-2021-05-01.zip \
# 		Tatoeba-MT-models/eng-gmw/opus1m+bt-2021-04-10.zip
# MODELS = 	Tatoeba-MT-models/roa-eng/opus1m+bt-2021-05-01.zip \
#		Tatoeba-MT-models/eus-eng/opus+bt-2021-04-30.zip
# MODELS = Tatoeba-MT-models/deu-tur/opusTCv20210807-2021-10-22.zip \
#	Tatoeba-MT-models/deu-ara/opusTCv20210807-2021-10-22.zip \
#	Tatoeba-MT-models/deu-hbs/opusTCv20210807-2021-10-10.zip \
#	Tatoeba-MT-models/deu-ron/opusTCv20210807-2021-10-22.zip

MODELS = 	Tatoeba-MT-models/gmw-eng/opus1m+bt-2021-05-01.zip \
		Tatoeba-MT-models/roa-eng/opus1m+bt-2021-05-01.zip \
		Tatoeba-MT-models/gmq-eng/opus1m+bt-2021-05-01.zip \
		Tatoeba-MT-models/zle-eng/opus1m+bt-2021-05-02.zip \



VERSION = 1.0.0

MODELS_DONE = $(patsubst %.zip,%.done,${MODELS})
METADATA_DONE = $(patsubst %.zip,%.metadone,${MODELS})


all: ${MODELS_DONE}
metadata: ${METADATA_DONE}

## don't run in parallel because we copy and remove model files
.NOTPARALLEL:

## docker image and metadata
${MODELS_DONE}:
	rm -fr models
	echo "${STORAGE_HOME}/${@:.done=.zip}" > models.txt
	./build_elg_image_and_metadata.sh \
		$(shell echo "$@" | cut -f1 -d/ | sed 's/-models//' | tr '[:upper:]' '[:lower:]') \
		$(shell echo '${@:.done=}' | cut -f2,3 -d/ | tr '+/' '__') \
		$(shell echo "$@" | cut -f2 -d/) \
		${shell echo $@ | sed 's/^.*[\-\_]\(....\-..\-..\)\.done$$/\1/' | tr '-' '.'}
	mkdir -p $(dir $@)
	touch $@
	rm -fr models

## meta data only
${METADATA_DONE}:
	rm -fr models
	echo "${STORAGE_HOME}/${@:.metadone=.zip}" > models.txt
	./build_elg_metadata.sh \
		$(shell echo "$@" | cut -f1 -d/ | sed 's/-models//' | tr '[:upper:]' '[:lower:]') \
		$(shell echo '${@:.metadone=}' | cut -f2,3 -d/ | tr '+/' '__') \
		$(shell echo "$@" | cut -f2 -d/) \
		${shell echo $@ | sed 's/^.*[\-\_]\(....\-..\-..\)\.done$$/\1/' | tr '-' '.'}
	mkdir -p $(dir $@)
	touch $@
	rm -fr models


sme:
	./build_elg_image_and_metadata.sh \
		opus-mt \
		opus_giella \
		sme-gmq \
		1.0.0 \
		"sme-se-fi sme-se-nb sme-se-nn sme-se-sv gmq-fi+nb+no+nn+sv-se"

