#-*-makefile-*-
#
#

## installation destinations
PREFIX   = /usr/local
BINDIR   = ${PREFIX}/bin
SHAREDIR = ${PREFIX}/share
CACHEDIR = /var/cache
LOGDIR   = /var/log


## model parameters
DATASET    = opus
SRC_LANGS  = de+fr+sv+en
TRG_LANGS  = et+hu+fi

MODEL_HOME = /media/letsmt/nmt/models
LANG_PAIR  = ${SRC_LANGS}-${TRG_LANGS}
NMT_MODEL  = ${MODEL_HOME}/${LANG_PAIR}/${DATASET}.bpe32k-bpe32k.enfi.transformer.model1.npz.best-perplexity.npz
NMT_VOCAB  = ${MODEL_HOME}/${LANG_PAIR}/${DATASET}.bpe32k-bpe32k.enfi.vocab.yml
BPEMODEL   = ${SHAREDIR}/opustrans/${DATASET}.${SRC_LANGS}.bpe32k-model
APPLYBPE   = ${BINDIR}/apply_bpe.py

OPUSTRANS_SERVER = ${BINDIR}/opustrans-server-cached.py
OPUSTRANS_CACHE  = ${CACHEDIR}/opustrans/${DATASET}.${LANGPAIR}.cache.db


## marian NMT build directory and binaries
MARIAN_BUILD = ${HOME}/marian/build
MARIAN_SERVER = ${MARIAN_BUILD}/marian-server


## server port and marian NMT parameters
## (beam size 2 and normalisation 1)
MARIAN_PORT = 11111
MARIAN_PARA = -b2 -n1


## installation tools
INSTALL = install -c
INSTALL_BIN = ${INSTALL} -m 755
INSTALL_DATA = ${INSTALL} -m 644


.PHONY: all
all: install-marian-server install-opustrans-server

.PHONY: install-marian-server install-opustrans-server
install-marian-server: /etc/init/marian-${DATASET}-${LANGPAIR}.conf
install-opustrans-server: /etc/init.d/opustrans-${DATASET}-${LANGPAIR}
# install-opustrans-server: /etc/init/opustrans-${DATASET}-${LANGPAIR}.conf


/etc/init/marian-${DATASET}-${LANGPAIR}.conf:
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


## service via sysvinit
/etc/init.d/opustrans-${DATASET}-${LANGPAIR}: ${OPUSTRANS_SERVER} ${APPLYBPE} ${BPEMODEL}
	sed 	-e 's#%%SERVICENAME%%#opustrans-server#' \
		-e 's#%%APPSHORTDESCR%%#opustrans-server#' \
		-e 's#%%APPLONGDESCR%%#translation service#' \
		-e 's#%%APPBIN%%#$<#' \
		-e 's#%%APPARGS%%#-c ${OPUSTRANS_CACHE} --bpe ${BPEMODEL}#' \
	< service-template > ${notdir $@}
	${INSTALL_BIN} ${notdir $@} $@
	rm -f ${notdir $@}
	update-rc.d ${notdir $@} defaults
	rm -f ${notdir $@}
	service ${notdir $@} start || true


## service via Ubuntu upstart (does not seem to work)
/etc/init/opustrans-${DATASET}-${LANGPAIR}.conf: ${OPUSTRANS_SERVER} ${APPLYBPE} ${BPEMODEL}
	mkdir -p ${dir ${OPUSTRANS_CACHE}}
	mkdir -p ${LOGDIR}/opustrans
	@echo 'description     "OpusTrans Server"'      > ${notdir $@}
	@echo ''                                       >> ${notdir $@}
	@echo 'start on filesystem or runlevel [2345]' >> ${notdir $@}
	@echo 'stop on shutdown'                       >> ${notdir $@}
	@echo ''                                       >> ${notdir $@}
	@echo 'respawn'                                >> ${notdir $@}
	@echo 'respawn limit 3 12'                     >> ${notdir $@}
	@echo ''                                       >> ${notdir $@}
	@echo "exec $< -c ${OPUSTRANS_CACHE} --bpe ${BPEMODEL} > ${LOGDIR}/opustrans/server.out 2> ${LOGDIR}/opustrans/server.err" >> ${notdir $@}
	${INSTALL_DATA} -b -S .old ${notdir $@} $@
	rm -f ${notdir $@}
	service ${notdir $(@:.conf=)} start || true



${BINDIR}/%: %
	${INSTALL_BIN} $< $@

${SHAREDIR}/opustrans/%: %
	mkdir -p ${dir $@}
	${INSTALL_DATA} $< $@
