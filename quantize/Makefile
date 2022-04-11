#-*-makefile-*-
#
#

## model parameters
SRC       ?= fin
TRG       ?= eng

SRC_LANGS ?= ${SRC}
TRG_LANGS ?= ${TRG}

LANGPAIR = ${SRC_LANGS}-${TRG_LANGS}


## repository with all public models
OPUSMT_MODEL_REPO  = https://object.pouta.csc.fi/OPUS-MT-models
TATOEBA_MODEL_REPO = https://object.pouta.csc.fi/Tatoeba-MT-models
MODEL_REPO = ${TATOEBA_MODEL_REPO}

## set model to be downloaded (the last model for the given language pair and dataset)
## TODO: check whether at least one exists!
## TODO: this always prefers +bt models even if they are not the last one

MODEL_PATTERN = .*\.zip
OPUSMT_MODEL := ${shell wget -q -O - ${MODEL_REPO}/index.txt | \
		grep '^${SRC_LANGS}-${TRG_LANGS}/${MODEL_PATTERN}' | \
		sort | tail -1}

##-------------------------------------------------------------------------------
## overwrite OPUSMT_MODEL or MODEL_URL if you want to download a specific model
##
##    make OPUSMT_MODEL=fi-en/modelname.zip ...
##    make MODEL_URL=https://download.server/fi-en/modelname.zip ...
##
##-------------------------------------------------------------------------------

## download URL of the model
MODEL_URL = ${MODEL_REPO}/${OPUSMT_MODEL}


## installation destinations
PREFIX   = /usr/local
BINDIR   = ${PREFIX}/bin
SHAREDIR = ${PREFIX}/share
CACHEDIR = /var/cache
LOGDIR   = /var/log

## home directories of MarianNMT models
MODEL_HOME = ${SHAREDIR}/opusMT/models


MODEL_RELEASE = ${shell echo "${OPUSMT_MODEL:.zip=}" |rev | cut -f1 -d_ | cut -f1-3 -d- | rev}
MODEL_CONFIG  = ${MODEL_HOME}/${LANGPAIR}/${MODEL_RELEASE}/config.yml


# marian-nmt binaries
MARIAN_SERVER  = ${BINDIR}/browsermt-marian-server
MARIAN_CONVERT = ${BINDIR}/browsermt-marian-conv

## server code
OPUSMT_ROUTER = ${BINDIR}/opusMT-router.py
OPUSMT_SERVER = ${BINDIR}/opusMT-server-cached.py
OPUSMT_CACHE  = ${CACHEDIR}/opusMT/${LANGPAIR}-${MODEL_RELEASE}.cache.db


## server port and marian NMT parameters
## (beam size 2 and normalisation 1)
PORT        ?= 10000
ROUTER_PORT ?= 8080
OPUSMT_PORT ?= ${PORT}
MARIAN_PORT ?= ${shell echo $$((${PORT} + 10000))}


## installation tools
INSTALL = install -c
INSTALL_BIN = ${INSTALL} -m 755
INSTALL_DATA = ${INSTALL} -m 644


.PHONY: all
all: opusMT-server opusMT-router

.PHONY: install
install: opusMT-server


${MARIAN_SERVER} ${MARIAN_CONVERT}:
	${MAKE} -C ../install $@

${BINDIR}/opusMT-server-cached.py: ../opusMT-server-cached.py
	${INSTALL_BIN} $< $@




## examples of short-cut targets for installing MT-services for specific language pairs
fien-server:
	${MAKE} SRC_LANGS=fi TRG_LANGS=en LANGPAIR=fin-eng PORT=10000 opusMT-server



.PHONY: install-server opusMT-server
install-server opusMT-server: install-marian-server install-opusMT-server


.PHONY: install-marian-server install-opusMT-server
install-marian-server: /etc/init.d/marian-${LANGPAIR}-${MODEL_RELEASE}
install-opusMT-server: /etc/init.d/opusMT-${LANGPAIR}-${MODEL_RELEASE}


.PHONY: fetch fetch-model download-model
fetch fetch-model download-model: ${MODEL_CONFIG}

.PHONY: test-download
test-download:
	make MODEL_HOME=. fetch-model


model-list.txt:
	wget -O model-list.txt ${MODEL_REPO}/index.txt

.PHONY: print-selected-model info
print-selected-model info:
	@echo ${OPUSMT_MODEL}
	@echo ${MODEL_URL}
	@echo ${MODEL_CONFIG}


## quantize model and create config file
${MODEL_CONFIG}: ${MARIAN_SERVER} ${MARIAN_CONVERT}
	wget -O model.zip ${MODEL_URL}
	mkdir -p model
	cd model && unzip ../model.zip
	mkdir -p ${dir $@}
	${INSTALL_DATA} model/* ${dir $@}
	${MARIAN_CONVERT} -g intgemm8 -f `ls ${dir $@}*.npz` -t ${dir $@}model-intgemm8.bin
	rm -f ${dir $@}*.npz
	cat ${dir $@}decoder.yml |\
	sed 	-e 's/- .*.npz/- model-intgemm8.bin/' \
		-e 's/beam-size: .*$$/beam-size: 1/' \
	> $@
	@echo ""                          >> $@
	@echo "skip-cost: true"           >> $@
	@echo 'gemm-precision: int8shift' >> $@
	@echo 'max-length-factor: 2.0'    >> $@
	if [ `find ${dir $@} -name '*.lex*.bin' | wc -l` -gt 0 ]; then \
	  l=`find ${dir $@} -name '*.lex*.bin' | head -1 | xargs basename`; \
	  echo 'shortlist:'              >> $@; \
	  echo "    - $$l"               >> $@; \
	  echo '    - false'             >> $@; \
	fi
	rm -f model/*
	rmdir model
	rm -f model.zip


## sentence piece model
## TODO: assumes that the first one can be used to pre-process source language
## TODO: assumes that we always have sentence piece models
SPM = $(firstword $(sort ${wildcard $(dir ${MODEL_CONFIG})*.spm}))


## opusMT service via sysvinit
/etc/init.d/opusMT-${LANGPAIR}-${MODEL_RELEASE}: ${OPUSMT_SERVER} ../service-template
	sed 	-e 's#%%SERVICENAME%%#opusMT-server-${LANGPAIR}-${MODEL_RELEASE}#' \
		-e 's#%%APPSHORTDESCR%%#opusMT-server#' \
		-e 's#%%APPLONGDESCR%%#translation service#' \
		-e 's#%%APPBIN%%#$<#' \
		-e 's#%%APPARGS%%#-p ${OPUSMT_PORT} -c ${OPUSMT_CACHE} --spm $(SPM) --mtport ${MARIAN_PORT} -s ${subst +, ,${SRC_LANGS}} -t ${subst +, ,${TRG_LANGS}}#' \
	  < ../service-template > ${notdir $@}
	mkdir -p ${dir ${OPUSMT_CACHE}}
	${INSTALL_BIN} ${notdir $@} $@
	rm -f ${notdir $@}
	update-rc.d ${notdir $@} defaults 60
	rm -f ${notdir $@}
	service ${notdir $@} restart


## opusMT service via sysvinit
/etc/init.d/marian-${LANGPAIR}-${MODEL_RELEASE}: ${MODEL_CONFIG} ../service-template
	sed 	-e 's#%%SERVICENAME%%#marian-server-${LANGPAIR}-${MODEL_RELEASE}#' \
		-e 's#%%APPSHORTDESCR%%#marian-server#' \
		-e 's#%%APPLONGDESCR%%#translation service#' \
		-e 's#%%APPBIN%%#${MARIAN_SERVER}#' \
		-e 's#%%APPARGS%%#--alignment -p ${MARIAN_PORT} -c ${MODEL_CONFIG}#' \
	< ../service-template > ${notdir $@}
	${INSTALL_BIN} ${notdir $@} $@
	rm -f ${notdir $@}
	update-rc.d ${notdir $@} defaults 20
	rm -f ${notdir $@}
	service ${notdir $@} restart
	sleep 5


remove remove-server: remove-marian-server remove-opusMT-server

remove-opusMT-server:
	service opusMT-${LANGPAIR}-${MODEL_RELEASE} stop || true
	update-rc.d -f opusMT-${LANGPAIR}-${MODEL_RELEASE} remove
	rm -f /etc/init.d/opusMT-${LANGPAIR}-${MODEL_RELEASE}

remove-marian-server:
	service marian-${LANGPAIR}-${MODEL_RELEASE} stop || true
	update-rc.d -f marian-${LANGPAIR}-${MODEL_RELEASE} remove
	rm -f /etc/init.d/marian-${LANGPAIR}-${MODEL_RELEASE}

