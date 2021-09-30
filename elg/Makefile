



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
# MODELS = 	Tatoeba-MT-models/eng-roa/opus1m+bt-2021-04-10.zip
VERSION = 1.0.0

MODELS_DONE = $(patsubst %.zip,%.done,${MODELS})


all: ${MODELS_DONE}

.NOTPARALLEL:

${MODELS_DONE}:
	rm -fr models
	echo "${STORAGE_HOME}/${@:.done=.zip}" > models.txt
	./build_elg_image_and_metadata.sh \
		$(shell echo "$@" | cut -f1 -d/ | sed 's/-models//' | tr '[:upper:]' '[:lower:]') \
		$(shell echo '${@:.done=}' | cut -f2,3 -d/ | tr '+/' '__') \
		${VERSION} \
		OPUS-MT-$(shell echo "$@" | cut -f2 -d/)
	mkdir -p $(dir $@)
	touch $@
	rm -fr models
