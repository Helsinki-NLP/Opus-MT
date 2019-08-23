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
MODEL_HOME = /media/letsmt/nmt/models
LANG_PAIR  = de+fr+sv+en-et+hu+fi
NMT_MODEL  = ${MODEL_HOME}/${LANG_PAIR}/opus-wmt.bpe32k-bpe32k.enfi.transformer.model1.npz.best-perplexity.npz
NMT_VOCAB  = ${MODEL_HOME}/${LANG_PAIR}/opus-wmt.bpe32k-bpe32k.enfi.vocab.yml
BPEMODEL   = ${SHAREDIR}/opentrans/opus.de+fr+sv+en.bpe32k-model
APPLYBPE   = ${BINDIR}/apply_bpe.py

OPENTRANS_SERVER = ${BINDIR}/opentrans-server-cached.py
OPENTRANS_CACHE  = ${CACHEDIR}/opentrans/opus.de+fr+sv+en.cache.db


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
all: install-marian-server install-opentrans-server

.PHONY: install-marian-server install-opentrans-server
install-marian-server: /etc/init/marian-server.conf
install-opentrans-server: /etc/init.d/opentrans
# install-opentrans-server: /etc/init/opentrans-server.conf


/etc/init/marian-server.conf:
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
/etc/init.d/opentrans: ${OPENTRANS_SERVER} ${APPLYBPE} ${BPEMODEL}
	sed 	-e 's#%%SERVICENAME%%#opentrans-server#' \
		-e 's#%%APPSHORTDESCR%%#opentrans-server#' \
		-e 's#%%APPLONGDESCR%%#translation service#' \
		-e 's#%%APPBIN%%#$<#' \
		-e 's#%%APPARGS%%#-c ${OPENTRANS_CACHE} --bpe ${BPEMODEL}#' \
	< service-template > ${notdir $@}
	${INSTALL_BIN} ${notdir $@} $@
	rm -f ${notdir $@}
	update-rc.d ${notdir $@} defaults
	rm -f ${notdir $@}
	service ${notdir $@} start || true


## service via Ubuntu upstart (does not seem to work)
/etc/init/opentrans-server.conf: ${OPENTRANS_SERVER} ${APPLYBPE} ${BPEMODEL}
	mkdir -p ${dir ${OPENTRANS_CACHE}}
	mkdir -p ${LOGDIR}/opentrans
	@echo 'description     "OpenTrans Server"'      > ${notdir $@}
	@echo ''                                       >> ${notdir $@}
	@echo 'start on filesystem or runlevel [2345]' >> ${notdir $@}
	@echo 'stop on shutdown'                       >> ${notdir $@}
	@echo ''                                       >> ${notdir $@}
	@echo 'respawn'                                >> ${notdir $@}
	@echo 'respawn limit 3 12'                     >> ${notdir $@}
	@echo ''                                       >> ${notdir $@}
	@echo "exec $< -c ${OPENTRANS_CACHE} --bpe ${BPEMODEL} > ${LOGDIR}/opentrans/server.out 2> ${LOGDIR}/opentrans/server.err" >> ${notdir $@}
	${INSTALL_DATA} -b -S .old ${notdir $@} $@
	rm -f ${notdir $@}
	service ${notdir $(@:.conf=)} start || true



${BINDIR}/%: %
	${INSTALL_BIN} $< $@

${SHAREDIR}/opentrans/%: %
	mkdir -p ${dir $@}
	${INSTALL_DATA} $< $@
