#!/bin/bash
#
# USAGE preprocess.sh langid bpecodes < input > output
#
#
# replace MOSESHOME and SPMENCODE with your own setup! 

if [ `hostname -d` == "bullx" ]; then
  APPLHOME=/projappl/project_2001569
  MOSESHOME=${APPLHOME}/mosesdecoder
  SPMENCODE=${APPLHOME}/marian-dev/build-spm/spm_encode
elif [ `hostname -d` == "csc.fi" ]; then
  APPLHOME=/proj/memad/tools
  MOSESHOME=/proj/nlpl/software/moses/4.0-65c75ff/moses
  SPMENCODE=${APPLHOME}/marian-dev/build-spm/spm_encode
else
  MOSESHOME=${PWD}/mosesdecoder
  SPMENCODE=${PWD}/marian-dev/build/spm_encode
fi

MOSESSCRIPTS=${MOSESHOME}/scripts
TOKENIZER=${MOSESSCRIPTS}/tokenizer


${TOKENIZER}/replace-unicode-punctuation.perl |
${TOKENIZER}/remove-non-printing-char.perl |
${TOKENIZER}/normalize-punctuation.perl -l $1 |
sed 's/  */ /g;s/^ *//g;s/ *$$//g' |
${SPMENCODE} --model $2
