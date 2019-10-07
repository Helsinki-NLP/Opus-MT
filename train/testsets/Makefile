

TXT = $(patsubst %.sgm,%,${wildcard *.sgm})

all: ${TXT}

${TXT}: %: %.sgm
	grep '</seg>' $< |\
	sed 's/<[^>]*>//g' |\
	sed 's/^ *//' |\
	sed 's/ *$$//' |\
	sed 's/  */ /g' |\
	sed	-e 's/&quot;/"/g' \
		-e 's/&gt;/>/g' \
		-e 's/&lt;/</g' \
		-e 's/&amp;/&/g' \
		-e "s/&apos;/'/g" > $@


fix:
	for s in ${wildcard *-src*}; do \
	  mv $$s `echo $$s | sed 's/-src//'`; \
	done
	for s in ${wildcard *-ref*}; do \
	  mv $$s `echo $$s | sed 's/-ref//'`; \
	done
