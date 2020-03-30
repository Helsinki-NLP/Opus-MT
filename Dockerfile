FROM debian:stable

WORKDIR /usr/src/app

# Install base packages
RUN set -eux; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
		ca-certificates git wget gnupg build-essential lsb-release g++ \
		automake autogen libtool cmake-data cmake unzip \
		libboost-all-dev libblas-dev libopenblas-dev libz-dev libssl-dev \
		libprotobuf17 protobuf-compiler libprotobuf-dev \
		python3-dev python3-pip python3-setuptools python3-websocket;

# Install Intel libraries
RUN set -eux; \
	wget https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB; \
	apt-key add GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB; \
	sh -c 'echo deb https://apt.repos.intel.com/mkl all main > /etc/apt/sources.list.d/intel-mkl.list';\
	apt-get update; \
	apt-get install -y --no-install-recommends \
		intel-mkl-64bit-2019.5-075; \
	rm -f GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB;

# Install Marian MT
RUN set -eux; \
	git clone https://github.com/marian-nmt/marian marian; \
	cd marian; \
	git checkout 1.9.0; \
	# Choose CPU or GPU(CUDA) from below lines.
	# cmake . -DCOMPILE_SERVER=on -DUSE_SENTENCEPIECE=on -DCOMPILE_CUDA=on -DUSE_STATIC_LIBS=on; \
	cmake . -DCOMPILE_SERVER=on -DUSE_SENTENCEPIECE=on -DCOMPILE_CPU=on -DCOMPILE_CUDA=off -DUSE_STATIC_LIBS=on; \
	make -j 2 install;

COPY . .

# Install python requirements.

RUN set -eux; \
	pip3 install -r requirements.txt

# install services
RUN install -m 755 marian/marian /usr/local/bin/; \
	install -m 755 marian/marian-server /usr/local/bin/; \
	install -m 755 marian/marian-server /usr/local/bin/; \
	install -m 755 marian/marian-vocab /usr/local/bin/; \
	install -m 755 marian/marian-decoder /usr/local/bin/; \
	install -m 755 marian/marian-scorer /usr/local/bin/; \
	install -m 755 marian/marian-conv /usr/local/bin/; \
	install -m 644 marian/libmarian.a  /usr/local/lib/;

EXPOSE 80
CMD python3 server.py -c services.json -p 80
