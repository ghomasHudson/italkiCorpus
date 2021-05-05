#!/bin/bash

function makefile {
    # Make json file in correct format
    i=1
    (while read p; do
        test $i -eq 1 && ((i=i+1)) && continue
        echo \{\"text\"\: \"$((sed $'s/[^[:print:]\t]//g' ../italki_data/$(echo $p | awk -F "," '{print $1}').txt ) | tr '"' ' ') \"\, \"label\"\:\"$(echo $p | awk -F "," '{print $3}')\"\}
    done <../italki_data/labels.$1.csv) > /tmp/$1.json
}

makefile train
makefile dev

pl-transformers-train task=nlp/text_classification dataset.cfg.train_file=/tmp/train.json dataset.cfg.validation_file=/tmp/dev.json
