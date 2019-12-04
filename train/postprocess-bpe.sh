#!/bin/bash
#
# USAGE postprocess.sh langid < input > output
#
#
# replace MOSESHOME with your own setup


if [ `hostname -d` == "bullx" ]; then
  APPLHOME=/projappl/project_2001569
  MOSESHOME=${APPLHOME}/mosesdecoder
elif [ `hostname -d` == "csc.fi" ]; then
  APPLHOME=/proj/memad/tools
  MOSESHOME=/proj/nlpl/software/moses/4.0-65c75ff/moses
else
  MOSESHOME=${PWD}/mosesdecoder
fi

MOSESSCRIPTS=${MOSESHOME}/scripts
TOKENIZER=${MOSESSCRIPTS}/tokenizer


sed 's/\@\@ //g;s/ \@\@//g;s/ \@\-\@ /-/g' |
${TOKENIZER}/detokenizer.perl -l $1
