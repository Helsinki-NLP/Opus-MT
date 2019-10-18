
PREFIX = /usr/local

INSTALL = install -c
INSTALL_BIN = ${INSTALL} -m 755
INSTALL_DATA = ${INSTALL} -m 644

UBUNTU_RELEASE = ${shell lsb_release -a | grep 'Release' | cut -f2}


.PHONY: all
all: ${PREFIX}/bin/marian-server



.PHONY: prereqs
prereqs: GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB
	sudo apt-key add $<
	sudo sh -c 'echo deb https://apt.repos.intel.com/mkl all main > /etc/apt/sources.list.d/intel-mkl.list'
	sudo apt-get -q update
	sudo apt-get -q upgrade g++
	sudo apt-get -q install automake autogen libtool cmake-data cmake unzip
	sudo apt-get -q install libboost-all-dev libblas-dev libopenblas-dev libz-dev libssl-dev
	sudo apt-get -q install python3-dev python3-pip python3-setuptools python3-websocket
	sudo apt-get -q install intel-mkl-64bit-2019.5-075
	sudo pip3 install SimpleWebSocketServer
	sudo pip3 install mosestokenizer pycld2 sqlitedict
ifeq (${UBUNTU_RELEASE},14.04)
	sudo apt-get -q install cmake3-data cmake3
	sudo pip3 install websocket-client==0.46.0
endif

GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB:
	wget https://apt.repos.intel.com/intel-gpg-keys/$@

gperftools:
	git clone https://github.com/gperftools/gperftools
	cd $@ && ./autogen.sh
	cd $@ && ./configure
	make -j 2 -C $@
	sudo make -j 2 -C $@ install


marian:
	sudo ${MAKE} /swapfile
	${MAKE} prereqs
	git clone https://github.com/marian-nmt/marian

marian/build/marian-server: marian
	${MAKE} gperftools
	mkdir -p ${dir $@}
	cd ${dir $@} && \
	cmake .. -DCMAKE_BUILD_TYPE=Release -DCOMPILE_CUDA=off -DUSE_STATIC_LIBS=on
	make -C ${dir $@}


${PREFIX}/bin/marian-server:
	${MAKE} marian/build/marian-server
	sudo ${INSTALL_BIN} marian/build/marian         ${PREFIX}/bin/marian
	sudo ${INSTALL_BIN} marian/build/marian-server  ${PREFIX}/bin/marian-server
	sudo ${INSTALL_BIN} marian/build/marian-vocab   ${PREFIX}/bin/marian-vocab
	sudo ${INSTALL_BIN} marian/build/marian-decoder ${PREFIX}/bin/marian-decoder
	sudo ${INSTALL_BIN} marian/build/marian-scorer  ${PREFIX}/bin/marian-scorer
	sudo ${INSTALL_BIN} marian/build/marian-conv    ${PREFIX}/bin/marian-conv
	sudo ${INSTALL_DATA} marian/build/libmarian.a   ${PREFIX}/lib/libmarian.a


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
