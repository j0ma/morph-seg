#! /usr/bin/env bash
set -euo pipefail

# TODO: Run "fi" sometime

run_lang () {
  lang=$1
  stem_bpe_size_lang=$2
  stem_bpe_size_en=$3
  word_bpe_size=$4
  source_dir="data/wordlists/${lang}_en/"
  output_dir="data/segmented/wmt19/morsel/${lang}_en"
  mkdir -p "$output_dir/$lang" "$output_dir/en"
  ./src/morsel-bpe.sh "$source_dir/train.${lang}.wordlist.noslash" "$stem_bpe_size_lang" "$word_bpe_size" "$output_dir/$lang" &> "$output_dir/$lang/run.log" &
  ./src/morsel-bpe.sh "$source_dir/train.en.wordlist.noslash" "$stem_bpe_size_en" "$word_bpe_size" "$output_dir/en" &> "$output_dir/en/run.log" &
  wait
  grep "MORSEL + BPE segmentation vocab size" "$output_dir"/*/run.log
}

run_lang kk 2050 1950 2500 &
run_lang gu 2400 2400 2500 &
wait
