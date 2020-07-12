#set -euo pipefail

LANG="$1"
DAMPENING="$2"

case "${LANG}" in
"en-all")
    INPUT_FILE="./data/raw/flores/flores.vocab.en.lowercase.withcounts"
    ;;
"en-ne")
    INPUT_FILE="./data/wordlists/ne_en/train.en.wordlist"
    ;;
"en-si")
    INPUT_FILE="./data/wordlists/si_en/train.en.wordlist"
    ;;
*)
    echo "Usage: tune-morfessor-baseline.sh <en-ne/en-si/en-all> <dampening/no-dampening>"
    exit 1
    ;;
esac

case "${DAMPENING}" in
"dampening")
    DAMP="ones"
    echo "Performing type-level tranining..."
    ;;
"no-dampening")
    DAMP="none"
    echo "Performing token-level tranining..."
    ;;
*)
    echo "Usage: tune-morfessor-baseline.sh <en-ne/en-si/en-all> <dampening/no-dampening>"
    exit 1
    ;;
esac

TRAIN_SCRIPT="./src/train-morfessor-baseline.py"
EVAL_SCRIPT="./src/eval-mc.sh"
OUTPUT_BASE="./tuning/morfessor-baseline/${DAMPENING}/${LANG}"
CORPUS_WEIGHTS=$(cat ./tuning/morfessor-baseline/corpus-weights)
MODEL_OUTPUT_FOLDER="./bin/morfessor-baseline-tuning"
GOLD_ANALYSES="./data/morpho-challenge/en/all_analyses"
TUNING_RESULTS_FILE="${OUTPUT_BASE}/tuning-results"
CONST_SEP=" + "
N_PAIRS=1000
LANG="en"

mkdir -p "${OUTPUT_BASE}"
mkdir -p "${MODEL_OUTPUT_FOLDER}"

#for cw in "0.1"; do

for cw in $CORPUS_WEIGHTS; do
    echo "Training with corpus weight: ${cw}"
    OUTPUT_FOLDER="${OUTPUT_BASE}/corpus-weight-${cw}"
    PREFIX="${OUTPUT_FOLDER}/mbl.corpusweight${cw}"
    SEGM_OUTPUT_FILE="${PREFIX}.segmentations.en"
    ANALYSES_FILE="${PREFIX}.analyses.en"
    WORDS_FILE="${PREFIX}.words.en"
    EVAL_SEGM_OUTPUT_FILE="${PREFIX}.segm4eval.en"

    python "${TRAIN_SCRIPT}" \
        --lang "${LANG}" \
        -i "${INPUT_FILE}" \
        -o "${OUTPUT_FOLDER}" \
        --dampening "${DAMP}" \
        --construction-separator "${CONST_SEP}" \
        --model-type batch-recursive \
        --model-output-folder "${MODEL_OUTPUT_FOLDER}" \
        --segmentation-output-file "${SEGM_OUTPUT_FILE}" \
        --corpus-weight "${cw}" \
        --lowercase

    echo "Creating MC2010 formatted segmentations..."

    # cut out the segmentations and the words
    tail -n +2 "${SEGM_OUTPUT_FILE}" |
        cut -f 2- -d " " |
        sed 's/ + / /g' |
        sort \
            >"${ANALYSES_FILE}"

    # join the segmentations to get the words in the same order
    tr -d ' ' \
        <"${ANALYSES_FILE}" \
        >"${WORDS_FILE}"

    paste \
        "${WORDS_FILE}" \
        "${ANALYSES_FILE}" \
        >"${EVAL_SEGM_OUTPUT_FILE}"

    echo "Computing F1..."

    bash ${EVAL_SCRIPT} \
        "${GOLD_ANALYSES}" \
        "${EVAL_SEGM_OUTPUT_FILE}" \
        "${N_PAIRS}" \
        "${PREFIX}"

    F1=$(
        tail -1 "${PREFIX}.score" |
            cut -d' ' -f3 |
            sed "s/%;//g"
    )

    printf "%s\t%s\n" "${cw}" "${F1}" >>"${TUNING_RESULTS_FILE}"

done
