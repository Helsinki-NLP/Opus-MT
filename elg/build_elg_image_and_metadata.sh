#!/bin/sh

set -x

rm -f image-name.txt

LANGS=$1

for src_lang in $LANGS; do
    src_lang_opt="--source-lang $(echo $src_lang | cut --delimiter="-" -f1)"
    src_region_opt=""
    if [[ "$src_lang" == *"-"* ]]; then
	src_region_opt="--source-region $(echo $src_lang | cut --delimiter="-" -f2)"
    fi
    for tgt_lang in $LANGS; do
	tgt_lang_opt="--target-lang $(echo $tgt_lang | cut --delimiter="-" -f1)"
	tgt_region_opt=""
	if [[ "$tgt_lang" == *"-"* ]]; then
	    tgt_region_opt="--target-region $(echo $tgt_lang | cut --delimiter="-" -f2)"
	fi
	if [ $src_lang = $tgt_lang ]; then continue; fi
	python3 generate_metadata.py $src_lang_opt $tgt_lang_opt $src_region_opt $trg_region_opt
    done
done
exit

rm -rf models
mkdir -p models
while read line; do
    wget $line
    mkdir -p models/$(basename $(dirname $line))
    unzip -o -d "models/$(basename $(dirname $line))" "$(basename $line)"
    rm "$(basename $line)"
done < models.txt
IMAGE_NAME=$(< image-name.txt)
sudo docker build . -t helsinkinlp/"$IMAGE_NAME"
