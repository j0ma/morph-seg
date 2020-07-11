#!/usr/bin/env bash
set -euo pipefail

OUT=tuning/morsel
mkdir -p "$OUT"

python src/tune_morsel.py MORSEL/params/dev.txt data/wordlists/en/brown.wordlist data/morpho-challenge/en/all_analyses "$OUT/brown" --workers 8 > "$OUT/brown_results.tsv"
python src/tune_morsel.py MORSEL/params/dev.txt data/wordlists/ne_en/train.en.wordlist data/morpho-challenge/en/all_analyses "$OUT/ne_en" --workers 8 > "$OUT/ne_en_results.tsv"
python src/tune_morsel.py MORSEL/params/dev.txt data/wordlists/si_en/train.en.wordlist data/morpho-challenge/en/all_analyses "$OUT/si_en" --workers 8 > "$OUT/si_en_results.tsv"
