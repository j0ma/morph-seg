#!/usr/bin/bash

# eval-morpho-challenge.sh
# (c) Jonne Saleva, 2020

if [[ "$#" != 3 ]]
then
    echo $#
    echo "Wrong number of command line arguments supplied!"
    echo "Usage: bash eval-morpho-challenge.sh <gold-std-file> <results-file> <gold-std-word-pairs-file>"
    exit 1
fi

GOLD_STD_FILE=$1
RESULTS_FILE=$2
GOLD_STD_PAIRS_PATH=$3

TMP=/tmp/mc-eval-$(date -I)
mkdir -p $TMP
RELEVANT_GOLD_PATH=$TMP/relevant-words.gold
RESULTS_PAIRS_PATH=$TMP/result.wordpairs

cut -f1 $GOLD_STD_FILE > $RELEVANT_GOLD_PATH

perl ./sample_word_pairs_v2.pl \
    -n 300 \
    -refwords $RELEVANT_GOLD_PATH \
    < $RESULTS_FILE > $RESULTS_PAIRS_PATH

perl eval_morphemes_v2.pl \
    $GOLD_STD_PAIRS_PATH \
    $RESULTS_PAIRS_PATH \
    $GOLD_STD_FILE \
    $RESULTS_FILE



