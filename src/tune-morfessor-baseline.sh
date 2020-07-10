INPUT_FILE="./data/raw/flores/flores.vocab.en.lowercase.withcounts"
INPUT_NOCOUNTS="./data/raw/flores/flores.vocab.en.lowercase"
TRAIN_SCRIPT="./src/train-morfessor-baseline.py"
EVAL_SCRIPT="./src/eval_mc.sh"
OUTPUT_BASE="./tuning/morfessor-baseline/"
CORPUS_WEIGHTS=$(cat ./tuning/morfessor-baseline/corpus-weights)
MODEL_OUTPUT_FOLDER="./bin/"
GOLD_ANALYSES="./data/morpho-challenge/en/all_analyses"
TUNING_RESULTS_FILE="${OUTPUT_BASE}/tuning-results"
CONST_SEP=" + "
N_PAIRS=1000
LANG="en"

for cw in $CORPUS_WEIGHTS; do
    echo "Training with corpus weight: ${cw}"
    OUTPUT_FOLDER="${OUTPUT_BASE}/corpus-weight-${cw}"
    SEGM_OUTPUT_FILE="${OUTPUT_FOLDER}/flores.vocab.en.lowercase.segmented.morfessor-baseline-batch-recursive.corpusweight${cw}"
    EVAL_SEGM_OUTPUT_FILE="${OUTPUT_FOLDER}/flores.vocab.en.lowercase.morfessor-baseline-batch-recursive.corpusweight${cw}.segm4eval.en"
    EVAL_PREFIX="${OUTPUT_FOLDER}/morfessor-baseline-batch-recursive.corpusweight${cw}"

    python "${TRAIN_SCRIPT}" \
        --lang "${LANG}" \
        -i "${INPUT_FILE}" \
        -o "${OUTPUT_FOLDER}" \
        --construction-separator "${CONST_SEP}" \
        --model-type batch-recursive \
        --model-output-folder "${MODEL_OUTPUT_FOLDER}" \
        --corpus-weight "${cw}" \
        --lowercase

    paste \
        "${INPUT_NOCOUNTS}" \
        "${SEGM_OUTPUT_FILE}" \
        >"${EVAL_SEGM_OUTPUT_FILE}"

    bash ${EVAL_SCRIPT} \
        "${GOLD_ANALYSES}" \
        "${EVAL_SEGM_OUTPUT_FILE}" \
        "${N_PAIRS}" \
        "${EVAL_PREFIX}"

    BLEU=$(
        tail -1 \
            "${OUTPUT_FOLDER}/morfessor-baseline-batch-recursive.corpusweight${cw}.score" |
            cut -d' ' -f3 | sed "s/%;//g"
    )

    printf "%s\t%s\n" "${cw}" "${BLEU}" >>"${TUNING_RESULTS_FILE}"

done
