#!/usr/bin/env bash
set -euo pipefail

# Example usage: ./src/morsel-bpe.sh data/raw/flores/flores.vocab.en.lowercase.withcounts 1800 2500 <output directory>
# The first BPE size number is what is used for the stems, which should be smaller than your desired output vocab size,
# since many of the stem-final units will need to be copied into a non-final version, increasing the vocab size.
# You will need to build MORSEL before running this. Run src/build-morsel.sh

wordlist=$1
stem_bpe_size=$2
word_bpe_size=$3
out_dir=$4

mkdir -p $out_dir

# Run MORSEL
java -XX:+UseSerialGC -jar MORSEL/target/morsel.jar "$wordlist" params/morsel/tuned.txt "$out_dir/morsel_analysis.txt" --segment > "$out_dir/morsel_log.txt"
# Make a copy of just the first two columns so Morpho Challenge (MC) evaluation can be run
cut -f 1-2 "$out_dir/morsel_analysis.txt" > "$out_dir/morsel_analysis_mc.txt"
# Process MORSEL's output into a proper segmentation and a dictionary of stems
python MORSEL/pymorsel/process_segmentation.py "$out_dir/morsel_analysis.txt" "$wordlist" "$out_dir/morsel_seg.txt" "$out_dir/stem_dict.txt"

# Learn a BPE code for the stems
subword-nmt learn-bpe -t -s "$stem_bpe_size" --dict-input -i "$out_dir/stem_dict.txt" -o "$out_dir/stem_code.txt"
# Apply the code to the stems
cut -f 1 -d " " "$out_dir/stem_dict.txt" > "$out_dir/stems.txt"
subword-nmt apply-bpe -i "$out_dir/stems.txt" -c "$out_dir/stem_code.txt" -o "$out_dir/stems_bpe.txt"
# Merge the stem BPE and the MORSEL segmentation
python MORSEL/pymorsel/apply_bpe_to_segmentation.py "$out_dir/morsel_seg.txt" "$out_dir/stems_bpe.txt" "$out_dir/morsel_seg_bpe_map.txt"
# Get the total size of the vocab
echo "MORSEL + BPE segmentation vocab size:" "$(cut -f 2 "$out_dir/morsel_seg_bpe_map.txt" | subword-nmt get-vocab | wc -l)"

# Also do pure BPE on the input for comparison
python src/convert_mc_wordlist_to_subword_nmt.py < "$wordlist" > "$out_dir/word_dict.txt"
cut -f 1 -d " " "$out_dir/word_dict.txt" > "$out_dir/words.txt"
subword-nmt learn-bpe -t -s "$word_bpe_size" --dict-input -i "$out_dir/word_dict.txt" -o "$out_dir/word_code.txt"
subword-nmt apply-bpe -i "$out_dir/words.txt" -c "$out_dir/word_code.txt" -o "$out_dir/words_bpe.txt"
# Make into a map
paste "$out_dir/words.txt" "$out_dir/words_bpe.txt" | sort > "$out_dir/words_bpe_map.txt"
echo "BPE segmentation vocab size:" "$(cut -f 2 "$out_dir/words_bpe_map.txt" | subword-nmt get-vocab | wc -l)"
