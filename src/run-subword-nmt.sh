SLUG="yiddish-lrec2020-romanized"
INPUT_FILE="../data/raw/${SLUG}"
CODES_FILE="../bin/${SLUG}-subword-nmt.bpe.codes"
OUTPUT_FILE="../data/segmented/${SLUG}.segmented.subword-nmt"
BPE_SIZE=5000

echo "Learning BPE..."
subword-nmt learn-bpe -s $BPE_SIZE < $INPUT_FILE > $CODES_FILE

echo "Segmenting with BPE..."
subword-nmt apply-bpe -c $CODES_FILE < $INPUT_FILE > $OUTPUT_FILE
