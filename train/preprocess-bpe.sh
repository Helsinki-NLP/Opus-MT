#!/bin/bash
#
# USAGE preprocess.sh langid bpecodes < input > output
#
#
# replace MOSESHOME and SNMTPATH with your own setup! 


if [ `hostname -d` == "bullx" ]; then
  APPLHOME=/projappl/project_2001569
  MOSESHOME=${APPLHOME}/mosesdecoder
  SNMTPATH=${APPLHOME}/subword-nmt/subword_nmt
elif [ `hostname -d` == "csc.fi" ]; then
  APPLHOME=/proj/memad/tools
  MOSESHOME=/proj/nlpl/software/moses/4.0-65c75ff/moses
  SNMTPATH=${APPLHOME}/subword-nmt
else
  MOSESHOME=${PWD}/mosesdecoder
  SNMTPATH=${PWD}/subword-nmt
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
