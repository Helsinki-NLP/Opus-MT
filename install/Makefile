
PREFIX = /usr/local

INSTALL = install -c
INSTALL_BIN = ${INSTALL} -m 755
INSTALL_DATA = ${INSTALL} -m 644

UBUNTU_RELEASE = ${shell lsb_release -a 2>/dev/null | grep 'Release' | cut -f2}


.PHONY: all install install-browsermt clean
all: marian/build/marian-server

install: ${PREFIX}/bin/marian-server
install-browsermt: ${PREFIX}/bin/browsermt-marian-server ${PREFIX}/bin/browsermt-marian-conv

marian:
	git clone https://github.com/marian-nmt/marian
	cd marian && git checkout 1.10.0

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


${PREFIX}/bin/marian-server: marian/build/marian-server
	sudo ${INSTALL_BIN} $< $@

#	sudo ${INSTALL_BIN} marian/build/marian         ${PREFIX}/bin/marian
#	sudo ${INSTALL_BIN} marian/build/marian-server  ${PREFIX}/bin/marian-server
#	sudo ${INSTALL_BIN} marian/build/marian-vocab   ${PREFIX}/bin/marian-vocab
#	sudo ${INSTALL_BIN} marian/build/marian-decoder ${PREFIX}/bin/marian-decoder
#	sudo ${INSTALL_BIN} marian/build/marian-scorer  ${PREFIX}/bin/marian-scorer
#	sudo ${INSTALL_BIN} marian/build/marian-conv    ${PREFIX}/bin/marian-conv
#	sudo ${INSTALL_DATA} marian/build/libmarian.a   ${PREFIX}/lib/libmarian.a




## marian-server from the browsermt fork

${PREFIX}/bin/browsermt-marian-server:
	${MAKE} browsermt/marian-dev/build/marian-server
	sudo ${INSTALL_BIN} browsermt/marian-dev/build/marian-server $@

${PREFIX}/bin/browsermt-marian-conv:
	${MAKE} browsermt/marian-dev/build/marian-conv
	sudo ${INSTALL_BIN} browsermt/marian-dev/build/marian-conv $@

browsermt/marian-dev:
	cd ${dir $@} && git clone https://github.com/browsermt/marian-dev

browsermt/marian-dev/build/marian-server: browsermt/marian-dev
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

browsermt/marian-dev/build/marian-conv: browsermt/marian-dev/build/marian-server
	@echo "done!"



# add libgoogle-perftools-dev instead of compiling from scratch

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
