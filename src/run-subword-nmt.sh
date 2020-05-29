<<<<<<< HEAD
INPUT_FILE="../data/raw/all-flores-words-nonumbers.en"
CODES_FILE="../tmp/subword-nmt.bpe.codes"
OUTPUT_FILE="../data/segmented/all-flores-words-nonumbers.en.segmented.subword-nmt"
=======
INPUT_FILE="../data/raw/brown_wordlist.wordonly.txt"
CODES_FILE="../tmp/subword-nmt.bpe.codes"
OUTPUT_FILE="../data/segmented/brown_wordlist.segmented.subword-nmt"
>>>>>>> 856af8cfbaad157e5fadf38111ea1048f98eb3bb
BPE_SIZE=5000

echo "Learning BPE..."
subword-nmt learn-bpe -s $BPE_SIZE < $INPUT_FILE > $CODES_FILE

echo "Segmenting with BPE..."
subword-nmt apply-bpe -c $CODES_FILE < $INPUT_FILE > $OUTPUT_FILE
