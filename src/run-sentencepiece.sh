SPM_TRAIN="sentencepiece/spm_train.py"
SPM_ENCODE="sentencepiece/spm_encode.py"
SLUG="yiddish-lrec2020-romanized"
INPUT_FILE="../data/raw/${SLUG}"
OUTPUT_FILE="../data/segmented/${SLUG}.segmented.sentencepiece"
MODEL_OUTPUT="../bin/${SLUG}-sentencepiece.bpe"
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
