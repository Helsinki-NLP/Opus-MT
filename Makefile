#-*-makefile-*-
#
#

## model parameters
DATASET   = opus
SRC_LANGS = fi
TRG_LANGS = en
# SRC_LANGS = de+fr+sv+en
# TRG_LANGS = et+hu+fi

LANGPAIR = ${SRC_LANGS}-${TRG_LANGS}


## repository with all public models
MODEL_REPO = https://object.pouta.csc.fi/OPUS-MT


## installation destinations
PREFIX   = /usr/local
BINDIR   = ${PREFIX}/bin
SHAREDIR = ${PREFIX}/share
CACHEDIR = /var/cache
LOGDIR   = /var/log

## home directories of MarianNMT models
MODEL_HOME = ${SHAREDIR}/opusMT/models
# MODEL_HOME = /media/letsmt/nmt/models


LANG_PAIR  = ${SRC_LANGS}-${TRG_LANGS}
NMT_MODEL  = ${MODEL_HOME}/${LANG_PAIR}/${DATASET}.npz
NMT_VOCAB  = ${MODEL_HOME}/${LANG_PAIR}/${DATASET}.vocab.yml
BPEMODEL   = ${MODEL_HOME}/${LANG_PAIR}/${DATASET}.bpe
APPLYBPE   = ${BINDIR}/apply_bpe.py

## server code
MARIAN_SERVER = ${BINDIR}/marian-server
OPUSMT_ROUTER = ${BINDIR}/opusMT-router.py
OPUSMT_SERVER = ${BINDIR}/opusMT-server-cached.py
OPUSMT_CACHE  = ${CACHEDIR}/opusMT/${DATASET}.${LANGPAIR}.cache.db
OPUSMT_CONFIG = ${SHAREDIR}/opusMT/opusMT-servers.json

OPUSMT_DEV_SERVER = ${BINDIR}/opusMT-server-cached-dev.py

## server port and marian NMT parameters
## (beam size 2 and normalisation 1)
ROUTER_PORT = 8080
OPUSMT_PORT = 20000
MARIAN_PORT = 10000
MARIAN_PARA = -b2 -n1
DEFAULT_SOURCE_LANG = ${firstword ${subst +, ,${SRC_LANGS}}}
DEFAULT_TARGET_LANG = ${lastword ${subst +, ,${TRG_LANGS}}}


## installation tools
INSTALL = install -c
INSTALL_BIN = ${INSTALL} -m 755
INSTALL_DATA = ${INSTALL} -m 644


.PHONY: all
all: opusMT-server opusMT-router


enfi-server:
	${MAKE} SRC_LANGS=en TRG_LANGS=fi MARIAN_PORT=10000 OPUSMT_PORT=20000 opusMT-server

fien-server:
	${MAKE} SRC_LANGS=fi TRG_LANGS=en MARIAN_PORT=10001 OPUSMT_PORT=20001 opusMT-server

svfi-server:
	${MAKE} SRC_LANGS=sv TRG_LANGS=fi MARIAN_PORT=10002 OPUSMT_PORT=20002 opusMT-server

fisv-server:
	${MAKE} SRC_LANGS=fi TRG_LANGS=sv MARIAN_PORT=10003 OPUSMT_PORT=20003 opusMT-server

defi-server:
	${MAKE} SRC_LANGS=de TRG_LANGS=fi MARIAN_PORT=10004 OPUSMT_PORT=20004 opusMT-server

fide-server:
	${MAKE} SRC_LANGS=fi TRG_LANGS=de MARIAN_PORT=10005 OPUSMT_PORT=20005 opusMT-server



.PHONY: opusMT-server opusMT-router
opusMT-server: install-marian-server install-opusMT-server
opusMT-router: install-opusMT-router

opusMT-devserver: /etc/init.d/opusMT-dev-${DATASET}-${LANGPAIR}


.PHONY: install-marian-server install-opusMT-server
install-marian-server: /etc/init.d/marian-${DATASET}-${LANGPAIR}
install-opusMT-server: /etc/init.d/opusMT-${DATASET}-${LANGPAIR}
install-opusMT-router: /etc/init.d/opusMT

# install-marian-server: /etc/init/marian-${DATASET}-${LANGPAIR}.conf
# install-opusMT-server: /etc/init/opusMT-${DATASET}-${LANGPAIR}.conf


.PHONY: download-model
download-model: ${NMT_MODEL}

## download the last model for the given language pair and dataset
## TODO: check whether at least one exists!
${NMT_MODEL}:
	wget -O model-list.txt ${MODEL_REPO}
	wget -O model.zip \
		${MODEL_REPO}/`tr "<>" "\n\n" < model-list.txt | \
		grep 'models/${SRC_LANGS}-${TRG_LANGS}/${DATASET}' |\
		sort | tail -1`
	mkdir -p model
	cd model && unzip ../model.zip
	mkdir -p ${dir $@}
	${INSTALL_DATA} model/*.npz $@
	${INSTALL_DATA} model/*.vocab.yml ${NMT_VOCAB}
	${INSTALL_DATA} model/*.bpe ${BPEMODEL}
	rm -f model/*
	rmdir model
	rm -f model.zip model-list.txt




## opusMT service via sysvinit
/etc/init.d/opusMT: ${OPUSMT_ROUTER} ${OPUSMT_CONFIG} service-template
	sed 	-e 's#%%SERVICENAME%%#opusMT#' \
		-e 's#%%APPSHORTDESCR%%#opusMT#' \
		-e 's#%%APPLONGDESCR%%#translation service#' \
		-e 's#%%APPBIN%%#$<#' \
		-e 's#%%APPARGS%%#-p ${ROUTER_PORT} -c ${OPUSMT_CONFIG} -s ${DEFAULT_SOURCE_LANG} -t ${DEFAULT_TARGET_LANG}#' \
	< service-template > ${notdir $@}
	mkdir -p ${dir ${OPUSMT_CACHE}}
	${INSTALL_BIN} ${notdir $@} $@
	rm -f ${notdir $@}
	update-rc.d ${notdir $@} defaults 80
	rm -f ${notdir $@}
	systemctl daemon-reload
	service ${notdir $@} restart


## opusMT service via sysvinit
/etc/init.d/opusMT-${DATASET}-${LANGPAIR}: ${OPUSMT_SERVER} ${APPLYBPE} ${BPEMODEL} service-template
	sed 	-e 's#%%SERVICENAME%%#opusMT-server-${DATASET}-${LANGPAIR}#' \
		-e 's#%%APPSHORTDESCR%%#opusMT-server#' \
		-e 's#%%APPLONGDESCR%%#translation service#' \
		-e 's#%%APPBIN%%#$<#' \
		-e 's#%%APPARGS%%#-p ${OPUSMT_PORT} -c ${OPUSMT_CACHE} --bpe ${BPEMODEL} --mtport ${MARIAN_PORT} -s ${subst +, ,${SRC_LANGS}} -t ${subst +, ,${TRG_LANGS}}#' \
	< service-template > ${notdir $@}
	mkdir -p ${dir ${OPUSMT_CACHE}}
	${INSTALL_BIN} ${notdir $@} $@
	rm -f ${notdir $@}
	update-rc.d ${notdir $@} defaults 60
	rm -f ${notdir $@}
	systemctl daemon-reload
	service ${notdir $@} restart


## opusMT service via sysvinit
/etc/init.d/marian-${DATASET}-${LANGPAIR}: ${NMT_MODEL} service-template
	sed 	-e 's#%%SERVICENAME%%#marian-server-${DATASET}-${LANGPAIR}#' \
		-e 's#%%APPSHORTDESCR%%#marian-server#' \
		-e 's#%%APPLONGDESCR%%#translation service#' \
		-e 's#%%APPBIN%%#${MARIAN_SERVER}#' \
		-e 's#%%APPARGS%%#-p ${MARIAN_PORT} ${MARIAN_PARA} -m ${NMT_MODEL} -v ${NMT_VOCAB} ${NMT_VOCAB}#' \
	< service-template > ${notdir $@}
	${INSTALL_BIN} ${notdir $@} $@
	rm -f ${notdir $@}
	update-rc.d ${notdir $@} defaults 20
	rm -f ${notdir $@}
	systemctl daemon-reload
	service ${notdir $@} restart
	sleep 2


remove-services: remove-marian-service remove-opusMT-service remove-opusMT-router

remove-opusMT-router:
	service opusMT stop || true
	update-rc.d -f opusMT remove
	rm -f /etc/init.d/opusMT

remove-opusMT-service:
	service opusMT-${DATASET}-${LANGPAIR} stop || true
	update-rc.d -f opusMT-${DATASET}-${LANGPAIR} remove
	rm -f /etc/init.d/opusMT-${DATASET}-${LANGPAIR}

remove-marian-service:
	service marian-${DATASET}-${LANGPAIR} stop || true
	update-rc.d -f marian-${DATASET}-${LANGPAIR} remove
	rm -f /etc/init.d/marian-${DATASET}-${LANGPAIR}


#########################################################################################

## marian server as upstart service (work on Ubuntu 14.04 like this)
/etc/init/marian-${DATASET}-${LANGPAIR}.conf: ${NMT_MODEL}
	@echo 'description     "MarianNMT Server"'      > ${notdir $@}
	@echo ''                                       >> ${notdir $@}
	@echo 'start on filesystem or runlevel [2345]' >> ${notdir $@}
	@echo 'stop on shutdown'                       >> ${notdir $@}
	@echo ''                                       >> ${notdir $@}
	@echo 'respawn'                                >> ${notdir $@}
	@echo 'respawn limit 3 12'                     >> ${notdir $@}
	@echo ''                                       >> ${notdir $@}
	@echo "exec ${MARIAN_SERVER} -p ${MARIAN_PORT} ${MARIAN_PARA} -m ${NMT_MODEL} -v ${NMT_VOCAB} ${NMT_VOCAB}" >> ${notdir $@}
	${INSTALL_DATA} -b -S .old ${notdir $@} $@
	rm -f ${notdir $@}
	service ${notdir $(@:.conf=)} start || true

## service via Ubuntu upstart (does not seem to work)
/etc/init/opusMT-${DATASET}-${LANGPAIR}.conf: ${OPUSMT_SERVER} ${APPLYBPE} ${BPEMODEL}
	mkdir -p ${dir ${OPUSMT_CACHE}}
	mkdir -p ${LOGDIR}/opusMT
	@echo 'description     "OpusMT Server"'      > ${notdir $@}
	@echo ''                                       >> ${notdir $@}
	@echo 'start on filesystem or runlevel [2345]' >> ${notdir $@}
	@echo 'stop on shutdown'                       >> ${notdir $@}
	@echo ''                                       >> ${notdir $@}
	@echo 'respawn'                                >> ${notdir $@}
	@echo 'respawn limit 3 12'                     >> ${notdir $@}
	@echo ''                                       >> ${notdir $@}
	@echo "exec $< -c ${OPUSMT_CACHE} --bpe ${BPEMODEL} > ${LOGDIR}/opusMT/server.out 2> ${LOGDIR}/opusMT/server.err" >> ${notdir $@}
	${INSTALL_DATA} -b -S .old ${notdir $@} $@
	rm -f ${notdir $@}
	service ${notdir $(@:.conf=)} start || true



${BINDIR}/%: %
	${INSTALL_BIN} $< $@

${SHAREDIR}/opusMT/%: %
	mkdir -p ${dir $@}
	${INSTALL_DATA} $< $@

