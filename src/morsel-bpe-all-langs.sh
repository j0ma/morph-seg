#! /usr/bin/env bash
set -euo pipefail

for lang in si ne;  do
  dir="data/segmented/flores/morsel/${lang}_en/"
  mkdir -p "$dir/$lang" "$dir/en"
  ./src/morsel-bpe.sh "data/wordlists/${lang}_en/train.${lang}.wordlist" 1900 2500 "$dir/$lang" &> "$dir/$lang/run.log" &
  ./src/morsel-bpe.sh "data/wordlists/${lang}_en/train.en.wordlist" 1800 2500 "$dir/en" &> "$dir/en/run.log" &
done
wait
