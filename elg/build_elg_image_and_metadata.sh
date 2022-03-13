#!/bin/bash

if [[ $(basename $(pwd)) != "elg" ]]; then
    echo "Run this script in the elg/ subdirectory."
fi

RESOURCE_NAME="OPUS-MT"
IMAGE_NAME="opus-mt"
MODEL_VERSION="1.0.0"
RAM_PER_MODEL=768

LANGS=""
PAIRS=""

MODEL_COUNT=0
MIN_TEST_SIZE=100
BLEU_THRESHOLD=20
CHRF_THRESHOLD=0.4


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

echo
for readme in $(find models/ -name "README.md"); do
    ((MODEL_COUNT+=1))
    # Parse README files, yaml would be nicer
    # xargs to trim whitespace :)

    THIS_SRC=$(echo "$readme" | cut -f2 -d/ | cut -d"-" -f1)
    THIS_SRC_LANGS=$(grep "\* source language" $readme | cut -d":" -f2 | xargs)
    THIS_TGT_LANGS=$(grep "\* target language" $readme | cut -d":" -f2 | xargs)

    echo "In $readme, found source languages ${THIS_SRC_LANGS} and target languages ${THIS_TGT_LANGS}"

    for tgt in $THIS_TGT_LANGS; do
	SRC_LANGS=''
	for src in $THIS_SRC_LANGS; do
	    ## get scores and size of the biggest test set
	    BLEU_SCORE=$(grep '^|' $readme | grep "${src}.${tgt}" | sort -t '|' -k5 -nr | cut -f3 -d'|' | head -1 | xargs)
	    CHRF_SCORE=$(grep '^|' $readme | grep "${src}.${tgt}" | sort -t '|' -k5 -nr | cut -f4 -d'|' | head -1 | xargs)
	    TEST_SIZE=$(grep '^|' $readme | grep "${src}.${tgt}" | sort -t '|' -k5 -nr | cut -f5 -d'|' | head -1 | xargs)
	    ## if we don't know the test set size: get the highest scores
	    ## and assume that the test set is big enough (old models)
	    if [[ "$TEST_SIZE" == "" ]]; then
		TEST_SIZE=$MIN_TEST_SIZE
		BLEU_SCORE=$(grep '^|' $readme | grep "${src}.${tgt}" | sort -t '|' -k3 -nr | cut -f3 -d'|' | head -1 | xargs)
		CHRF_SCORE=$(grep '^|' $readme | grep "${src}.${tgt}" | sort -t '|' -k4 -nr | cut -f4 -d'|' | head -1 | xargs)
	    fi
	    echo "$src-$tgt: $BLEU_SCORE / $CHRF_SCORE / $TEST_SIZE"
	    if [[ "$TEST_SIZE" -ge $MIN_TEST_SIZE ]]; then
		if [[ "$BLEU_SCORE" != "" ]]; then
		    if [[ "$CHRF_SCORE" != "" ]]; then
			if (( $(echo "$BLEU_SCORE > $BLEU_THRESHOLD" | bc -l) )) || (( $(echo "$CHRF_SCORE > $CHRF_THRESHOLD" | bc -l) )); then
			    SRC_LANGS+="$src+"
			fi
		    fi
		fi
	    fi
	done
	if [[ "$SRC_LANGS" != "" ]]; then
	    echo "... add $THIS_SRC-$SRC_LANGS-$tgt"
	    SRC_LANGS=$(echo $SRC_LANGS | sed 's/\+$//')
	    PAIRS+="$THIS_SRC-$SRC_LANGS-$tgt "
	fi
    done
done
LANGS=$(echo "$PAIRS" | tr '\-\+' '  ' | tr ' ' "\n" | sort -u | xargs)

echo "supported pairs: ${PAIRS}"
echo "supported languages: $LANGS"
echo





TAG_NAME=$(echo $LANGS | tr ' ' '\n' | sort -u | tr '\n' ' ' | xargs | tr ' ' '-')"-"$(date +%F)
if [[ "$#" -ge 1 ]]; then
    IMAGE_NAME=$1
fi
if [[ "$#" -ge 2 ]]; then
    TAG_NAME=$2
fi
if [[ "$#" -ge 3 ]]; then
    GENERAL_LANGUAGE_PAIR=$3
fi
if [[ "$#" -ge 4 ]]; then
    MODEL_VERSION=$4
fi


## increase size per model if necessary
if [[ $MODEL_COUNT -gt 0 ]]; then
    MODEL_SIZE=$((`du -hsm models | cut -f1` / $MODEL_COUNT))
    if [[ $MODEL_SIZE -gt 400 ]]; then
	RAM_PER_MODEL=2048
    fi
fi


if ls *.xml 1> /dev/null 2>&1; then
    read -p "There are stale xml files present. Delete them? [y/n] " yn
    case $yn in
	[Yy]* ) rm -f *.xml;;
	* ) echo "OK, exiting so you can deal with them."; exit;;
    esac
fi

for pair in $PAIRS; do
    python3 generate_metadata.py \
	    --version $MODEL_VERSION \
	    --source-langs $(echo $pair | cut -d"-" -f2) \
	    --source-lang $(echo $pair | cut -d"-" -f1) \
    	    --target-lang $(echo $pair | cut -d"-" -f3) \
	    --image-name ${IMAGE_NAME}:${TAG_NAME} \
	    --models-in-image $MODEL_COUNT \
	    --ram-per-model $RAM_PER_MODEL
done
rm -f metadata_${IMAGE_NAME}_${TAG_NAME}.zip
zip metadata_${IMAGE_NAME}_${TAG_NAME}.zip *.xml
rm -f *.xml
echo "Wrote metadata in metadata_${IMAGE_NAME}_${TAG_NAME}.zip"

IMAGE_NAME="helsinkinlp/$IMAGE_NAME:$TAG_NAME"
echo "Building with name "$IMAGE_NAME


cd ..
# sudo docker build . -f Dockerfile.base -t opus-mt-base

# This is an annoying hack needed to deal with the fact that elg/ is in the
# main .dockerignore, and some files needed by the Dockerfile for elg live
# in the main directory. We copy those files, use them, then delete them.

cp server.py content_processor.py write_configuration.py apply_bpe.py elg/
cd elg
python3 write_configuration.py --source-lang-from-path > services.json
sudo docker build . -t $IMAGE_NAME
rm server.py content_processor.py write_configuration.py apply_bpe.py \
   services.json


sudo docker login
sudo docker push $IMAGE_NAME

# read -p "Want to push image to Dockerhub now? [y/n] " yn
#     case $yn in
# 	[Yy]* )
# 	    sudo docker login
# 	    sudo docker push $IMAGE_NAME;;
# 	* ) echo "Not pushing.";;
#     esac

echo
echo "Done. Don't forget to upload metadata_$IMAGE_NAME_$TAG_NAME.zip to the ELG catalogue!"
