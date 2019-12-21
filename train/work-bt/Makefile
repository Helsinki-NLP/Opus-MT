
LOAD_MODULES = 	module use -a /projappl/nlpl/software/modules/etc/ && \
		module load nlpl-udpipe nlpl-opus &&

WIKILANGS = 	${sort $(patsubst >%wiki-,%,${shell grep -o '>..wiki-' index.html})} \
		${sort $(patsubst >%wiki-,%,${shell grep -o '>...wiki-' index.html})}


LANGID   = af
WIKI_TXT = wiki.${LANGID}.gz

LANGNAME = ${shell ${LOAD_MODULES} opus-iso639 -e ${LANGID} | \
		cut -f1 -d';' | tr ' ' '-' | tr '[:upper:]' '[:lower:]'}
UDPIPE_MODEL = ${notdir $(shell find ${UDPIPE_MODELS}/ -name "${LANGNAME}*.udpipe" | head -1)}
WIKI_JSON = $(shell grep -o '${LANGID}wiki-[0-9]*-cirrussearch-content.json.gz' index.html | head -1)


all: index.html
	for l in ${WIKILANGS}; do \
	  ${MAKE} LANGID=$$l wiki-txt; \
	done

wiki-txt:
	if [ "${UDPIPE_MODEL}" != "" ]; then \
	  ${MAKE} ${WIKI_TXT}; \
	fi

print-names:
	echo ${LANGNAME}
	echo ${UDPIPE_MODEL}
	echo ${WIKI_JSON}


${WIKI_JSON}:
	wget https://dumps.wikimedia.org/other/cirrussearch/current/${WIKI_JSON}


${WIKI_TXT}: ${WIKI_JSON}
	${LOAD_MODULES} \
	zcat $< | jq -r '.text' | \
	grep -v 'null' |\
	udpipe --input=horizontal --tokenize \
	${UDPIPE_MODELS}/${UDPIPE_MODEL} |\
	grep '^\# *text *= *' |\
	sed 's/^\# *text *= *//' |\
	gzip -c > $@

index.html:
	wget -O $@ https://dumps.wikimedia.org/other/cirrussearch/current





# afrikaans-afribooms-ud-2.4-190531.udpipe	af
# ancient_greek-perseus-ud-2.4-190531.udpipe
# ancient_greek-proiel-ud-2.4-190531.udpipe
# arabic-padt-ud-2.4-190531.udpipe	ar
# armenian-armtdp-ud-2.4-190531.udpipe
# basque-bdt-ud-2.4-190531.udpipe		eo
# belarusian-hse-ud-2.4-190531.udpipe
# bulgarian-btb-ud-2.4-190531.udpipe		bg
# catalan-ancora-ud-2.4-190531.udpipe		ca
# chinese-gsd-ud-2.4-190531.udpipe		zh
# classical_chinese-kyoto-ud-2.4-190531.udpipe	zh_tw
# coptic-scriptorium-ud-2.4-190531.udpipe
# croatian-set-ud-2.4-190531.udpipe		hr
# czech-cac-ud-2.4-190531.udpipe		cs
# czech-cltt-ud-2.4-190531.udpipe		cs
# czech-fictree-ud-2.4-190531.udpipe		cs
# czech-pdt-ud-2.4-190531.udpipe		cs
# danish-ddt-ud-2.4-190531.udpipe		da
# dutch-alpino-ud-2.4-190531.udpipe		nl
# dutch-lassysmall-ud-2.4-190531.udpipe		nl
# english-ewt-ud-2.4-190531.udpipe		en
# english-gum-ud-2.4-190531.udpipe		en
# english-lines-ud-2.4-190531.udpipe		en
# english-partut-ud-2.4-190531.udpipe		en
# estonian-edt-ud-2.4-190531.udpipe		et
# estonian-ewt-ud-2.4-190531.udpipe		et
# finnish-ftb-ud-2.4-190531.udpipe		fi
# finnish-tdt-ud-2.4-190531.udpipe		fi
# french-gsd-ud-2.4-190531.udpipe		fr
# french-partut-ud-2.4-190531.udpipe		fr
# french-sequoia-ud-2.4-190531.udpipe		fr
# french-spoken-ud-2.4-190531.udpipe		fr
# galician-ctg-ud-2.4-190531.udpipe		gl
# galician-treegal-ud-2.4-190531.udpipe		gl
# german-gsd-ud-2.4-190531.udpipe		de
# gothic-proiel-ud-2.4-190531.udpipe
# greek-gdt-ud-2.4-190531.udpipe		el
# hebrew-htb-ud-2.4-190531.udpipe		he
# hindi-hdtb-ud-2.4-190531.udpipe		hi
# hungarian-szeged-ud-2.4-190531.udpipe		hu
# indonesian-gsd-ud-2.4-190531.udpipe		id
# irish-idt-ud-2.4-190531.udpipe		cy
# italian-isdt-ud-2.4-190531.udpipe		it
# italian-partut-ud-2.4-190531.udpipe		it
# italian-postwita-ud-2.4-190531.udpipe		it
# italian-vit-ud-2.4-190531.udpipe		it
# japanese-gsd-ud-2.4-190531.udpipe		ja
# korean-gsd-ud-2.4-190531.udpipe		ko
# korean-kaist-ud-2.4-190531.udpipe		ko
# latin-ittb-ud-2.4-190531.udpipe		la
# latin-perseus-ud-2.4-190531.udpipe		la
# latin-proiel-ud-2.4-190531.udpipe		la
# latvian-lvtb-ud-2.4-190531.udpipe		lv
# lithuanian-alksnis-ud-2.4-190531.udpipe	lt
# lithuanian-hse-ud-2.4-190531.udpipe		lt
# maltese-mudt-ud-2.4-190531.udpipe		mt
# marathi-ufal-ud-2.4-190531.udpipe
# north_sami-giella-ud-2.4-190531.udpipe
# norwegian-bokmaal-ud-2.4-190531.udpipe	nb
# norwegian-nynorsklia-ud-2.4-190531.udpipe	nn
# norwegian-nynorsk-ud-2.4-190531.udpipe	nn
# old_church_slavonic-proiel-ud-2.4-190531.udpipe
# old_french-srcmf-ud-2.4-190531.udpipe
# old_russian-torot-ud-2.4-190531.udpipe
# persian-seraji-ud-2.4-190531.udpipe		fa
# polish-lfg-ud-2.4-190531.udpipe		pl
# polish-pdb-ud-2.4-190531.udpipe		pl
# portuguese-bosque-ud-2.4-190531.udpipe	pt
# portuguese-gsd-ud-2.4-190531.udpipe		pt
# romanian-nonstandard-ud-2.4-190531.udpipe	ro
# romanian-rrt-ud-2.4-190531.udpipe		ro
# russian-gsd-ud-2.4-190531.udpipe		ru
# russian-syntagrus-ud-2.4-190531.udpipe	ru
# russian-taiga-ud-2.4-190531.udpipe		ru
# serbian-set-ud-2.4-190531.udpipe		sr
# slovak-snk-ud-2.4-190531.udpipe		sk
# slovenian-ssj-ud-2.4-190531.udpipe		sl
# slovenian-sst-ud-2.4-190531.udpipe		sl
# spanish-ancora-ud-2.4-190531.udpipe		es
# spanish-gsd-ud-2.4-190531.udpipe		es
# swedish-lines-ud-2.4-190531.udpipe		sv
# swedish-talbanken-ud-2.4-190531.udpipe	sv
# tamil-ttb-ud-2.4-190531.udpipe
# telugu-mtg-ud-2.4-190531.udpipe
# turkish-imst-ud-2.4-190531.udpipe		tr
# ukrainian-iu-ud-2.4-190531.udpipe
# urdu-udtb-ud-2.4-190531.udpipe
# uyghur-udt-ud-2.4-190531.udpipe
# vietnamese-vtb-ud-2.4-190531.udpipe		vi
# wolof-wtb-ud-2.4-190531.udpipe




# https://dumps.wikimedia.org/other/cirrussearch/current/afwiki-20191209-cirrussearch-content.json.gz
# https://dumps.wikimedia.org/other/cirrussearch/current/afwiki-20191209-cirrussearch-general.json.gz

# https://dumps.wikimedia.org/other/cirrussearch/current/afwikibooks-20191209-cirrussearch-content.json.gz
# https://dumps.wikimedia.org/other/cirrussearch/current/afwikibooks-20191209-cirrussearch-general.json.gz

# https://dumps.wikimedia.org/other/cirrussearch/current/afwikiquote-20191209-cirrussearch-content.json.gz
# https://dumps.wikimedia.org/other/cirrussearch/current/afwikiquote-20191209-cirrussearch-general.json.gz

# https://dumps.wikimedia.org/other/cirrussearch/current/afwiktionary-20191209-cirrussearch-content.json.gz
# https://dumps.wikimedia.org/other/cirrussearch/current/afwiktionary-20191209-cirrussearch-general.json.gz


# enwiki-20191209-cirrussearch-content.json.gz       10-Dec-2019 11:04         22622822308
# enwiki-20191209-cirrussearch-content.json.gz.tmp   10-Dec-2019 10:57         21460369408
# enwiki-20191209-cirrussearch-general.json.gz       10-Dec-2019 16:22         50406322974
# enwiki-20191209-cirrussearch-general.json.gz.tmp   10-Dec-2019 15:50         44720914432
# enwikibooks-20191209-cirrussearch-content.json.gz  10-Dec-2019 16:24           319454731
# enwikibooks-20191209-cirrussearch-general.json.gz  10-Dec-2019 16:25            97206925
# enwikinews-20191209-cirrussearch-content.json.gz   10-Dec-2019 16:26            53746769
# enwikinews-20191209-cirrussearch-general.json.gz   10-Dec-2019 16:36           364098656
# enwikiquote-20191209-cirrussearch-content.json.gz  10-Dec-2019 16:38           234637326
# enwikiquote-20191209-cirrussearch-general.json.gz  10-Dec-2019 16:38            66848855
# enwikisource-20191209-cirrussearch-content.json.gz 10-Dec-2019 17:09          5236203374
# enwikisource-20191209-cirrussearch-content.json..> 10-Dec-2019 17:06          4597481472
# enwikisource-20191209-cirrussearch-general.json.gz 10-Dec-2019 17:11           152492247
# enwikiversity-20191209-cirrussearch-content.jso..> 10-Dec-2019 17:12           145288148
# enwikiversity-20191209-cirrussearch-general.jso..> 10-Dec-2019 17:13           193051475
# enwikivoyage-20191209-cirrussearch-content.json.gz 10-Dec-2019 17:14           179134384
# enwikivoyage-20191209-cirrussearch-general.json.gz 10-Dec-2019 17:15            99357806
# enwiktionary-20191209-cirrussearch-content.json.gz 10-Dec-2019 17:36          2319801836
# enwiktionary-20191209-cirrussearch-content.json..> 10-Dec-2019 17:23           918503424
# enwiktionary-20191209-cirrussearch-general.json.gz 10-Dec-2019 17:42           848846623
# enwiktionary-20191209-cirrussearch-general.json..> 10-Dec-2019 17:40           661585920
