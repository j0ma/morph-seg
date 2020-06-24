#!/bin/bash

SLUG=$1
CORPUS_NAME=$2

for VAR in "${SLUG}" "${CORPUS_NAME}"
do
    if [ -z "${VAR}" ]
    then
        echo "Usage: bash ./run-subword-nmt.sh <slug> <corpus_name>"
        exit 1
    fi
done

RAW_DATA_ROOT="../data/raw/${CORPUS_NAME}"
SEGM_DATA_ROOT="../data/segmented/${CORPUS_NAME}"
INPUT_FILE="${RAW_DATA_ROOT}/${SLUG}"
OUTPUT_FILE="${SEGM_DATA_ROOT}/${SLUG}.segmented.subword-nmt"
CODES_FILE="../bin/${SLUG}-subword-nmt.bpe.codes"
BPE_SIZE=5000

echo "Learning BPE..."
subword-nmt learn-bpe -t -s "${BPE_SIZE}" < "${INPUT_FILE}" > "${CODES_FILE}"

echo "Segmenting with BPE..."
subword-nmt apply-bpe -c "${CODES_FILE}" < "${INPUT_FILE}" > "${OUTPUT_FILE}"
