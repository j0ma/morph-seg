#!/bin/bash

# handle command line args
SLUG=$1
CORPUS_NAME=$2
LANG=$3

for VAR in "${SLUG}" "${CORPUS_NAME}" "${LANG}"
do
    if [ -z "${VAR}" ]
    then
        echo "Usage: bash ./run-sentencepiece.sh <slug> <corpus_name> <lang>"
        exit 1
    fi
done

# handle train minlen based on language
if [ "${LANG}" = "si" ]
then
    TRAIN_MINLEN=6  # remove sentences with <6 BPE tokens
else
    TRAIN_MINLEN=1
fi
TRAIN_MAXLEN=250  # remove sentences with >250 BPE tokens

# script constants
SPM_TRAIN="sentencepiece/spm_train.py"
SPM_ENCODE="sentencepiece/spm_encode.py"

# paths etc
RAW_DATA_ROOT="../data/raw/${CORPUS_NAME}"
SEGM_DATA_ROOT="../data/segmented/${CORPUS_NAME}"
INPUT_FILE="${RAW_DATA_ROOT}/${SLUG}"
OUTPUT_FILE="${SEGM_DATA_ROOT}/${SLUG}.segmented.subword-nmt"
MODEL_OUTPUT="../bin/${SLUG}-sentencepiece.bpe"
BPE_SIZE=5000

python "${SPM_TRAIN}" \
    --input="${INPUT_FILE}" \
    --model_prefix="${MODEL_OUTPUT}" \
    --vocab_size="${BPE_SIZE}" \
    --character_coverage=1.0 \
    --model_type=bpe

python "${SPM_ENCODE}" \
    --model "${MODEL_OUTPUT}".model \
    --inputs "${INPUT_FILE}" \
    --outputs "${OUTPUT_FILE}" \
    --output_format=piece \
    --min-len "${TRAIN_MINLEN}" \
    --max-len "${TRAIN_MAXLEN}"
