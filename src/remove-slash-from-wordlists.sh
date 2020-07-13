#!/bin/bash

ROOT=$(pwd)
for pair in "ne_en" "si_en"
do
    cd "${ROOT}/data/wordlists/${pair}" || exit
    for lang in ${pair//_/ }
    do
        grep -v "[0-9]\s[\/\\]$" \
            "./train.${lang}.wordlist" \
            > "./train.${lang}.wordlist.noslash"
    done
done
