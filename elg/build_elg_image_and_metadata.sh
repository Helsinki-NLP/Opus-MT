#!/bin/bash

MODEL_VERSION="1.1"
LANGS=""
PAIRS=""

if [[ ! -d "models" ]]; then
    echo "models/ doesn't exist, creating it and fetching models listed in models.txt"
    mkdir models
    while read line; do
	# fetch and unpack each model
	wget $line
	mkdir -p models/$(basename $(dirname $line))
	unzip -o -d "models/$(basename $(dirname $line))" "$(basename $line)"
	rm "$(basename $line)"
    done < models.txt
else
    echo "Using existing directory models/"
fi

for readme in $(find models/ -name "README.md"); do
    # Parse README files, yaml would be nicer
    # xargs to trim whitespace :)
    THIS_SRC_LANGS=$(grep "source language" $readme | cut --delimiter=":" -f2 | xargs)
    THIS_TGT_LANGS=$(grep "target language" $readme | cut --delimiter=":" -f2 | xargs)
    echo "In $readme, found source languages ${THIS_SRC_LANGS} and target languages ${THIS_TGT_LANGS}"

    for src in $THIS_SRC_LANGS; do
	$LANGS+="$src "
	for tgt in $THIS_TGT_LANGS; do
	    PAIRS+="$src-$tgt "
	    LANGS+="$tgt "
	done
    done
done

echo "Ended up with pairs ${PAIRS}"

for pair in $PAIRS; do
    src_lang_opt="--source-lang $(echo $pair | cut --delimiter="-" -f1)"
    tgt_lang_opt="--target-lang $(echo $pair | cut --delimiter="-" -f2)"
    # src_region and tgt_region aren't used in Tatoeba, but generate_metadata knows about them
    python3 generate_metadata.py $src_lang_opt $tgt_lang_opt $src_region_opt $trg_region_opt
done

IMAGE_NAME="opus-mt-elg-"$(echo $LANGS | tr ' ' '\n' | sort -u | tr '\n' ' ' | xargs | tr ' ' '-')
if [[ "$#" -ge 1 ]]; then
    IMAGE_NAME=$1
fi

IMAGE_NAME="helsinkinlp/$IMAGE_NAME:$MODEL_VERSION"

echo "Building with name "$IMAGE_NAME
   
sudo docker build . -t $IMAGE_NAME
sudo docker login
sudo docker push $IMAGE_NAME
