
PREFIX = /usr/local

INSTALL = install -c
INSTALL_BIN = ${INSTALL} -m 755
INSTALL_DATA = ${INSTALL} -m 644



.PHONY: all
all: ${PREFIX}/bin/marian



.PHONY: prereqs
prereqs:
	sudo apt-get -q update
	sudo apt-get -q upgrade g++
	sudo apt-get -q install automake autogen libtool cmake
	sudo apt-get -q install libboost-all-dev libblas-dev libopenblas-dev libz-dev libssl-dev

gperftools:
	${MAKE} prereqs
	git clone https://github.com/gperftools/gperftools
	cd $@ && ./autogen.sh
	cd $@ && ./configure
	make -j 2 -C $@
	sudo make -j 2 -C $@ install

l_mkl_2019.4.243: l_mkl_2019.4.243.tgz
	tar -xzf $<
	cd $@ && sudo ./install.sh

marian: 
	git clone https://github.com/marian-nmt/marian

marian/build/marian: gperftools marian
	if [ -e l_mkl_2019.4.243.tgz ]; then \
	  ${MAKE} l_mkl_2019.4.243; \
	fi
	cd ${dir $@} && \
	cmake .. -DCMAKE_BUILD_TYPE=Release -DCOMPILE_CUDA=off -DUSE_STATIC_LIBS=on
	make -C ${dir $@}


${PREFIX}/bin/marian:
	${MAKE} marian/build/marian
	sudo ${INSTALL_BIN} marian/build/marian         $@
	sudo ${INSTALL_BIN} marian/build/marian-vocab   $@-vocab
	sudo ${INSTALL_BIN} marian/build/marian-decoder $@-decoder
	sudo ${INSTALL_BIN} marian/build/marian-scorer  $@-scorer
	sudo ${INSTALL_BIN} marian/build/marian-server  $@-server
	sudo ${INSTALL_BIN} marian/build/marian-conv    $@-conv
	sudo ${INSTALL_DATA} ${dir $<}/libmarian.a ${PREFIX}/lib/libmarian.a


cleanup:
	rm -fr marian
	rm -fr l_mkl_2019.4.243
	rm -fr gperftools
