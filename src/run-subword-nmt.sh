INPUT_FILE="../data/raw/all-flores-words-nonumbers.en"
CODES_FILE="../tmp/subword-nmt.bpe.codes"
OUTPUT_FILE="../data/segmented/all-flores-words-nonumbers.en.segmented.subword-nmt"
BPE_SIZE=5000

echo "Learning BPE..."
subword-nmt learn-bpe -s $BPE_SIZE < $INPUT_FILE > $CODES_FILE

echo "Segmenting with BPE..."
subword-nmt apply-bpe -c $CODES_FILE < $INPUT_FILE > $OUTPUT_FILE
