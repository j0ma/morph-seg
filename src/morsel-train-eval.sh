#!/usr/bin/env bash
set -euo pipefail

wordlist=$1
params=$2
gold_analyses=$3
out_dir=$4

mkdir -p "$out_dir"

# Run MORSEL
java -XX:+UseSerialGC -jar MORSEL/target/morsel.jar "$wordlist" "$params" "$out_dir/analysis.txt" > "$out_dir/log.txt" 2> "$out_dir/err.txt"
# Evaluate
src/eval-mc.sh "$gold_analyses" "$out_dir/analysis.txt" 1000 "$out_dir/eval"
# Extract the F-measure
tail -n 1 "$out_dir/eval.score" | grep -Eo "F-measure: [0-9.]+" | cut -f2 -d " "
