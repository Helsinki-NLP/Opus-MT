#!/bin/bash
#
# USAGE preproces.sh langid bpecodes < input > output
#

if [ `hostname -d` == "bullx" ]; then
  APPLHOME=/projappl/project_2001569
  MOSESHOME=${APPLHOME}/mosesdecoder
  SNMTPATH=${APPLHOME}/subword-nmt/subword_nmt
else
  APPLHOME=/proj/memad/tools
  MOSESHOME=/proj/nlpl/software/moses/4.0-65c75ff/moses
  SNMTPATH=${APPLHOME}/subword-nmt
fi

MOSESSCRIPTS=${MOSESHOME}/scripts
TOKENIZER=${MOSESSCRIPTS}/tokenizer


THREADS=4

${TOKENIZER}/replace-unicode-punctuation.perl |
${TOKENIZER}/remove-non-printing-char.perl |
${TOKENIZER}/normalize-punctuation.perl -l $1 |
${TOKENIZER}/tokenizer.perl -a -threads ${THREADS} -l $1 |
sed 's/  */ /g;s/^ *//g;s/ *$$//g' |
python3 ${SNMTPATH}/apply_bpe.py -c $2
