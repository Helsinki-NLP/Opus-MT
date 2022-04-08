
PREFIX = /usr/local
BINDIR   = ${PREFIX}/bin
SHAREDIR = ${PREFIX}/share
CACHEDIR = /var/cache
LOGDIR   = /var/log

INSTALL = install -c
INSTALL_BIN = ${INSTALL} -m 755
INSTALL_DATA = ${INSTALL} -m 644

UBUNTU_RELEASE = ${shell lsb_release -a 2>/dev/null | grep 'Release' | cut -f2}


## how to grep the model ULR from the JSON file
## if LANGPAIR is set then only take models for that language pair
## otherwise: take all

ifdef LANGPAIR
  GREP_MODEL = grep '"url":' | grep ${LANGPAIR} | cut -f2-3 -d: | sed 's/^ *\"\(.*\)\", *$$/\1/'
else
  GREP_MODEL = grep '"url":' | cut -f2-3 -d: | sed 's/^ *\"\(.*\)\", *$$/\1/'
endif


## get the model URL from the repository

MODEL_JSON := https://object.pouta.csc.fi/OPUS-MT-models/app/models.json
MODEL_URLS := ${shell wget -qq -O - ${MODEL_JSON} | ${GREP_MODEL}}


MODEL_URL = ${firstword ${MODEL_URLS}}
MODEL_NAME = $(patsubst %.tar.gz,%,${notdir ${MODEL_URL}})
MODEL_LANGPAIR = $(firstword $(subst ., ,${notdir ${MODEL_URL}}))
MODEL_SRCLANG = $(firstword $(subst -, ,${MODEL_LANGPAIR}))
MODEL_TRGLANG = $(lastword $(subst -, ,${MODEL_LANGPAIR}))


## supported source and target languages

SRC_LANGS ?= ${MODEL_SRCLANG}
TRG_LANGS ?= ${MODEL_TRGLANG}


## install location for OPUS-MT models

MODEL_HOME   = ${SHAREDIR}/opusMT_browserMT/models
MODEL_CONFIG = ${MODEL_HOME}/${MODEL_LANGPAIR}/${MODEL_NAME}/config.yml

MARIAN_SERVER = ${BINDIR}/browsermt-marian-server
OPUSMT_SERVER = ${BINDIR}/opusMT-server-cached.py
OPUSMT_CACHE  = ${CACHEDIR}/opusMT/browsermt.${LANGPAIR}.cache.db


## server ports (one fo marian-nmt and one for opusMT (pre- and post-processing)

PORT        ?= 10000
OPUSMT_PORT ?= ${PORT}
MARIAN_PORT ?= ${shell echo $$((${PORT} + 10000))}



.PHONY: all install clean
all: marian/build/marian-server


eng-ukr:
	${MAKE} LANGPAIR=eng-ukr SRC_LANGS=en TRG_LANGS=uk PORT=30000 opusMT-server

ukr-eng:
	${MAKE} LANGPAIR=ukr-eng SRC_LANGS=uk TRG_LANGS=en PORT=30001 opusMT-server



## print some info about the model that has been selected
info:
	@echo ${MODEL_URL}
	@echo ${MODEL_LANGPAIR}
	@echo ${MODEL_SRCLANG}
	@echo ${MODEL_TRGLANG}
	@echo ${MODEL_CONFIG}

.PHONY: opusMT-server install-marian install-marian-server install-opusMT-server
opusMT-server: install-marian-server install-opusMT-server

install-marian: ${MARIAN_SERVER}
install-marian-server: /etc/init.d/browsermt-marian-${MODEL_LANGPAIR}
install-opusMT-server: /etc/init.d/opusMT-browsermt-${MODEL_LANGPAIR}



.PHONY: remove remove-server remove-opusMT-server remove-marian-server
remove remove-server: remove-marian-server remove-opusMT-server

remove-opusMT-server:
	service opusMT-browsermt-${MODEL_LANGPAIR} stop || true
	update-rc.d -f opusMT-browsermt-${MODEL_LANGPAIR} remove
	rm -f /etc/init.d/opusMT-browsermt-${MODEL_LANGPAIR}

remove-marian-server:
	service browsermt-marian-${MODEL_LANGPAIR} stop || true
	update-rc.d -f browsermt-marian-${MODEL_LANGPAIR} remove
	rm -f /etc/init.d/browsermt-marian-${MODEL_LANGPAIR}




## download the model and move to model-home
.PHONY: fetch
fetch: ${MODEL_CONFIG}

${MODEL_CONFIG}:
	wget -O model.tar.gz ${MODEL_URL}
	mkdir -p ${dir $@}
	tar -C ${MODEL_HOME}/${MODEL_LANGPAIR} -xzf model.tar.gz
	ln -s ${dir $@}config*.yml $@
	chmod 755 ${dir $@}
	chmod 644 ${dir $@}*
	rm -f model.tar.gz




## marian-nmt service via sysvinit
/etc/init.d/browsermt-marian-${MODEL_LANGPAIR}: ${MODEL_CONFIG} ${MARIAN_SERVER} ../service-template
	sed 	-e 's#%%SERVICENAME%%#marian-server-${MODEL_LANGPAIR}#' \
		-e 's#%%APPSHORTDESCR%%#marian-server-${MODEL_LANGPAIR}#' \
		-e 's#%%APPLONGDESCR%%#translation service for ${MODEL_LANGPAIR}#' \
		-e 's#%%APPBIN%%#${MARIAN_SERVER}#' \
		-e 's#%%APPARGS%%#-p ${MARIAN_PORT} -c ${MODEL_CONFIG}#' \
	< ../service-template > ${notdir $@}
	${INSTALL_BIN} ${notdir $@} $@
	rm -f ${notdir $@}
	update-rc.d ${notdir $@} defaults 20
	rm -f ${notdir $@}
	service ${notdir $@} restart
	sleep 5


## opusMT service via sysvinit
/etc/init.d/opusMT-browsermt-${LANGPAIR}: ${OPUSMT_SERVER} ../service-template
	sed 	-e 's#%%SERVICENAME%%#opusMT-server-browsermt-${LANGPAIR}#' \
		-e 's#%%APPSHORTDESCR%%#opusMT-server-browsermt-${LANGPAIR}#' \
		-e 's#%%APPLONGDESCR%%#translation service for ${LANGPAIR}#' \
		-e 's#%%APPBIN%%#$<#' \
		-e 's#%%APPARGS%%#-p ${OPUSMT_PORT} -c ${OPUSMT_CACHE} --mtport ${MARIAN_PORT} -s ${subst +, ,${SRC_LANGS}} -t ${subst +, ,${TRG_LANGS}}#' \
	< ../service-template > ${notdir $@}; \
	mkdir -p ${dir ${OPUSMT_CACHE}}
	${INSTALL_BIN} ${notdir $@} $@
	rm -f ${notdir $@}
	update-rc.d ${notdir $@} defaults 60
	rm -f ${notdir $@}
	service ${notdir $@} restart





${OPUSMT_SERVER}: ${BINDIR}/%: ../%
	${INSTALL_BIN} $< $@


.PHONY: build-marian
build-marian: marian/build/marian-server

marian:
	git clone https://github.com/browsermt/marian-dev
	mv marian-dev marian

marian/build/marian-server: marian
	sudo ${MAKE} /swapfile
	sudo ${MAKE} prereqs
	${MAKE} gperftools
	mkdir -p ${dir $@}
ifeq (${UBUNTU_RELEASE},20.04)
	cd ${dir $@} && \
	cmake .. -DCMAKE_BUILD_TYPE=Release -DUSE_STATIC_LIBS=on -DCOMPILE_SERVER=on -DCOMPILE_CPU=on -DCOMPILE_CUDA=off
else
	cd ${dir $@} && \
	cmake .. -DCMAKE_BUILD_TYPE=Release -DUSE_STATIC_LIBS=on -DCOMPILE_SERVER=on -DUSE_SENTENCEPIECE=on -DCOMPILE_CPU=on -DCOMPILE_CUDA=off
endif
	${MAKE} -C ${dir $@} -j4



${PREFIX}/bin/browsermt-marian-server: marian/build/marian-server
	sudo ${INSTALL_BIN} $< $@


# TODO: add libgoogle-perftools-dev instead of compiling from scratch

.PHONY: prereqs
prereqs: GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB
	apt-key add $<
	sh -c 'echo deb https://apt.repos.intel.com/mkl all main > /etc/apt/sources.list.d/intel-mkl.list'
	apt-get -q update
	apt-get -q upgrade g++
	apt-get -q install automake autogen libtool cmake-data cmake unzip
	apt-get -q install libboost-all-dev libblas-dev libopenblas-dev libz-dev libssl-dev
	apt-get -q install python3-dev python3-pip python3-setuptools python3-websocket
	apt-get -q install intel-mkl-64bit-2019.5-075
ifeq (${UBUNTU_RELEASE},20.04)
	apt-get install libprotobuf-dev libsentencepiece-dev
endif
	pip3 install SimpleWebSocketServer
ifeq (${UBUNTU_RELEASE},16.04)
	pip3 install mosestokenizer==1.0.0
endif
ifeq (${UBUNTU_RELEASE},14.04)
	apt-get -q install cmake3-data cmake3
	pip3 install mosestokenizer==1.0.0
	pip3 install websocket-client==0.46.0
endif
	pip3 install mosestokenizer pycld2 sqlitedict
	pip3 install sentencepiece


GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB:
	wget https://apt.repos.intel.com/intel-gpg-keys/$@

gperftools:
	git clone https://github.com/gperftools/gperftools
	cd $@ && ./autogen.sh
	cd $@ && ./configure
	${MAKE} -j 2 -C $@
	sudo ${MAKE} -j 2 -C $@ install


/swapfile:
	fallocate -l 8G /swapfile
	chmod 600 /swapfile
	mkswap /swapfile
	swapon /swapfile
	grep -v '/swapfile' /etc/fstab > fstab.tmp
	echo '/swapfile   none    swap    sw    0   0' >> fstab.tmp
	${INSTALL_DATA} -b -S .old fstab.tmp /etc/fstab
	rm -f fstab.tmp


clean:
	rm -f GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB
	rm -fr marian
	rm -fr gperftools
