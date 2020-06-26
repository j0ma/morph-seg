#!/usr/bin/env bash
set -euo pipefail

# Evaluate system output (test_analyses) against the Morpho Challenge gold standard (gold_analyses) using
# n_pairs word pairs, outputting files starting with output_prefix.
#
# For the English data, using 1000 pairs is recommended.

gold_analyses=$1
test_analyses=$2
n_pairs=$3
output_prefix=$4

gold_words=${output_prefix}.goldwords
test_words=${output_prefix}.testwords
gold_pairs=${output_prefix}.goldpairs
test_pairs=${output_prefix}.testpairs
score=${output_prefix}.score

# Get gold/test words
cut -f1 "$gold_analyses" > "$gold_words"
cut -f1 "$test_analyses" > "$test_words"

# Generate gold/test pairs
src/morpho-challenge/sample_word_pairs_v2.pl -n "$n_pairs" -refwords "$test_words" < "$gold_analyses" > "$gold_pairs"
src/morpho-challenge/sample_word_pairs_v2.pl -n "$n_pairs" -refwords "$gold_words" < "$test_analyses" > "$test_pairs"

# Evaluate
src/morpho-challenge/eval_morphemes_v2.pl "$gold_pairs" "$test_pairs" "$gold_analyses" "$test_analyses" > "$score"
