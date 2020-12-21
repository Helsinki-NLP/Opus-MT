#!/bin/bash

mkdir -p models

while read line; do
    wget $line
    mkdir -p models/$(basename $(dirname $line))
    unzip -o -d "models/$(basename $(dirname $line))" "$(basename $line)"
    rm "$(basename $line)"
done < models.txt

