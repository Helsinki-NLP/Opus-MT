

MODELS = ${shell find . -type f -name '*.zip'}


## fix decoder.yml to match the typical setup 
## and the names of the model and vocab in the zip file

fix-config:
	for m in ${MODELS}; do \
	  f=`unzip -l $$m | grep -oi '[^ ]*npz'`; \
	  v=`unzip -l $$m | grep -oi '[^ ]*vocab.yml'`; \
	  echo 'models:' > decoder.yml; \
	  echo "  - $$f" >> decoder.yml; \
	  echo 'vocabs:' >> decoder.yml; \
	  echo "  - $$v" >> decoder.yml; \
	  echo "  - $$v" >> decoder.yml; \
	  echo 'beam-size: 6' >> decoder.yml; \
	  echo 'normalize: 1' >> decoder.yml; \
	  echo 'word-penalty: 0' >> decoder.yml; \
	  echo 'mini-batch: 1' >> decoder.yml; \
	  echo 'maxi-batch: 1' >> decoder.yml; \
	  echo 'maxi-batch-sort: src' >> decoder.yml; \
	  echo 'relative-paths: true' >> decoder.yml; \
	  zip $$m decoder.yml; \
	done
	rm -f decoder.yml


