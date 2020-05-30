SPM_TRAIN="sentencepiece/spm_train.py"
SPM_ENCODE="sentencepiece/spm_encode.py"
MODEL_OUTPUT="../tmp/sentencepiece.bpe"
INPUT_FILE="../data/raw/yiddish-lrec2020-romanized"
OUTPUT_FILE="../data/segmented/yiddish-lrec2020-romanized.segmented.sentencepiece"
BPE_SIZE=5000

python $SPM_TRAIN \
    --input=$INPUT_FILE \
    --model_prefix=$MODEL_OUTPUT \
    --vocab_size=$BPE_SIZE \
    --character_coverage=1.0 \
    --model_type=bpe

python $SPM_ENCODE \
    --model $MODEL_OUTPUT.model \
    --inputs $INPUT_FILE \
    --outputs $OUTPUT_FILE \
    --output_format=piece \
    --min-len 1 --max-len 250
