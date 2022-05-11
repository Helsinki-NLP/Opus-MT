#-*-makefile-*-
#
# recipes for installing MT servers at the University of Helsinki


## model configuration file
UH_MODEL_CONFIG = opusMT-servers-UH.json

.PHONY: opusMT-UH
opusMT-UH: ${SHAREDIR}/opusMT/${UH_MODEL_CONFIG}
	${MAKE} -C .. OPUSMT_CONFIG=$< opusMT-router

.PHONY: opusMT-UH-SSL
opusMT-UH-SSL: ${SHAREDIR}/opusMT/${UH_MODEL_CONFIG}
	${MAKE} -C .. OPUSMT_CONFIG=$< opusMT-ssl-router


## short-cut targets for installing MT-services for other language pairs
enfi-server:
	${MAKE} -C .. SRC_LANGS=en TRG_LANGS=fi MARIAN_PORT=10000 OPUSMT_PORT=20000 opusMT-server

fien-server:
	${MAKE} -C .. SRC_LANGS=fi TRG_LANGS=en MARIAN_PORT=10001 OPUSMT_PORT=20001 opusMT-server

svfi-server:
	${MAKE} -C .. SRC_LANGS=sv TRG_LANGS=fi MARIAN_PORT=10002 OPUSMT_PORT=20002 opusMT-server

fisv-server:
	${MAKE} -C .. SRC_LANGS=fi TRG_LANGS=sv MARIAN_PORT=10003 OPUSMT_PORT=20003 opusMT-server

defi-server:
	${MAKE} -C .. SRC_LANGS=de TRG_LANGS=fi MARIAN_PORT=10004 OPUSMT_PORT=20004 opusMT-server

fide-server:
	${MAKE} -C .. SRC_LANGS=fi TRG_LANGS=de MARIAN_PORT=10005 OPUSMT_PORT=20005 opusMT-server

frfi-server:
	${MAKE} -C .. SRC_LANGS=fr TRG_LANGS=fi MARIAN_PORT=11100 OPUSMT_PORT=21100 opusMT-server

fifr-server:
	${MAKE} -C .. SRC_LANGS=fi TRG_LANGS=fr MARIAN_PORT=11101 OPUSMT_PORT=21101 opusMT-server

enbcl-server:
	${MAKE} -C .. MODEL_PATTERN=${DATASET}\+nt\+bt.*\.zip \
		SRC_LANGS=en TRG_LANGS=bcl MARIAN_PORT=15000 OPUSMT_PORT=25000 opusMT-server



## special server for the Goethe Institute
defi-goethe-server:
	${MAKE} -C .. DATASET=goethe SRC_LANGS=de TRG_LANGS=fi MARIAN_PORT=10006 OPUSMT_PORT=20006 opusMT-server




etfi-scandinavian-server:
	${MAKE} -C .. SRC_LANGS="et+fi" TRG_LANGS="da+fo+is+no+nb+nn+sv" MARIAN_PORT=11000 OPUSMT_PORT=21000 opusMT-server

scandinavian-etfi-server:
	${MAKE} -C .. SRC_LANGS="da+fo+is+no+nb+nn+sv" TRG_LANGS="et+fi" MARIAN_PORT=11001 OPUSMT_PORT=21001 opusMT-server

etfi-germanic-server:
	${MAKE} -C .. SRC_LANGS="et+fi" TRG_LANGS="de+af+fy+nl" MARIAN_PORT=11002 OPUSMT_PORT=21002 opusMT-server

germanic-etfi-server:
	${MAKE} -C .. SRC_LANGS="de+af+fy+nl" TRG_LANGS="et+fi" MARIAN_PORT=11003 OPUSMT_PORT=21003 opusMT-server

germanic-server:
	${MAKE} -C .. SRC_LANGS="de+af+fy+nl" TRG_LANGS="de+af+fy+nl" MARIAN_PORT=11004 OPUSMT_PORT=21004 opusMT-server


romance-server:
	${MAKE} -C .. SRC_LANGS="ca+es+fr+ga+it+la+oc+pt_br+pt" TRG_LANGS="ca+es+fr+ga+it+la+oc+pt_br+pt" \
		MARIAN_PORT=11005 OPUSMT_PORT=21005 opusMT-server


celtic-english-server: opusMT-server-celtic-english
english-celtic-server: opusMT-server-english-celtic
celtic-english-update: update-model-celtic-english
english-celtic-update: update-model-english-celtic



%-celtic-english:
	${MAKE} -C .. SRC_LANGS="ga+cy+br+gd+kw+gv" TRG_LANGS="en" \
		DATASET=opus+techiaith \
		MARIAN_PORT=11050 OPUSMT_PORT=21050 ${@:-celtic-english=}

%-english-celtic:
	${MAKE} -C .. TRG_LANGS="ga+cy+br+gd+kw+gv" SRC_LANGS="en" \
		DATASET=opus+techiaith \
		MARIAN_PORT=11051 OPUSMT_PORT=21051 ${@:-english-celtic=}


# celtic-english-server:
# 	${MAKE} -C .. SRC_LANGS="ga+cy+br+gd+kw+gv" TRG_LANGS="en" \
# 		DATASET=opus+techiaith \
# 		MARIAN_PORT=11050 OPUSMT_PORT=21050 opusMT-server

# english-celtic-server:
# 	${MAKE} -C .. TRG_LANGS="ga+cy+br+gd+kw+gv" SRC_LANGS="en" \
# 		DATASET=opus+techiaith \
# 		MARIAN_PORT=11051 OPUSMT_PORT=21051 opusMT-server

sami-server: opusMT-server-sami
%-sami:
	${MAKE} -C .. SRC_LANGS="se+sma+smj+smn+sms+vep+et+fi+kv+krl+nb+no+nn+ru+sv+en" \
		TRG_LANGS="se+sma+smj+smn+sms+vep+et+fi+kv+krl+nb+no+nn+ru+sv+en" \
		DATASET=opus+giella \
		MARIAN_PORT=12000 OPUSMT_PORT=22000 ${@:-sami=}

# se+sma+smj+smn+sms-fi+nb+no+nn+ru+sv+en

## installation tools
INSTALL = install -c
INSTALL_BIN = ${INSTALL} -m 755
INSTALL_DATA = ${INSTALL} -m 644

${SHAREDIR}/opusMT/%: %
	mkdir -p ${dir $@}
	${INSTALL_DATA} $< $@

