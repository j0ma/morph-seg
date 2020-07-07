#!/usr/bin/env bash
set -euxo pipefail

# Example usage: ./src/morsel-bpe.sh data/raw/flores/flores.vocab.en.lowercase.withcounts 2500 <output directory>
# You will need to build MORSEL before running this. Run src/build-morsel.sh

wordlist=$1
bpe_size=$2
out_dir=$3

mkdir -p $out_dir

java -jar MORSEL/target/morsel.jar "$wordlist" MORSEL/params/dev.txt "$out_dir/morsel_analysis.txt" --segment --base-inf > "$out_dir/morsel_log.txt"
cut -f 1-2 "$out_dir/morsel_analysis.txt" > "$out_dir/morsel_analysis_clean.txt"
python MORSEL/pymorsel/process_segmentation.py "$out_dir/morsel_analysis.txt" "$wordlist" "$out_dir/segmentation.txt" "$out_dir/dict.txt"
# TODO: Adjust BPE size by the number of affixes
subword-nmt learn-bpe -t -s "$bpe_size" --dict-input -i "$out_dir/dict.txt" -o "$out_dir/code.txt"
cut -f 1 -d " " "$out_dir/dict.txt" > "$out_dir/dict_words.txt"
subword-nmt apply-bpe -i "$out_dir/dict_words.txt" -c "$out_dir/code.txt" -o "$out_dir/dict_bpe.txt"
python MORSEL/pymorsel/apply_bpe_to_segmentation.py "$out_dir/segmentation.txt" "$out_dir/dict_bpe.txt" "$out_dir/bpe_segmentation.txt"
