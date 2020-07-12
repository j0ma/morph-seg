#!/bin/bash

set -eo pipefail

# Created by argbash-init v2.8.1
# ARG_OPTIONAL_SINGLE([lang])
# ARG_OPTIONAL_SINGLE([lexicon-size])
# ARG_OPTIONAL_SINGLE([input-path])
# ARG_OPTIONAL_SINGLE([corpus-name])
# ARG_OPTIONAL_SINGLE([segmentation-output-path])
# ARG_OPTIONAL_SINGLE([seed-segmentation-input-path])
# ARG_OPTIONAL_SINGLE([model-output-path])
# ARG_OPTIONAL_SINGLE([min-shift-remainder])
# ARG_OPTIONAL_SINGLE([length-threshold])
# ARG_OPTIONAL_SINGLE([perplexity-threshold])
# ARG_OPTIONAL_SINGLE([min-perplexity-length])
# ARG_OPTIONAL_SINGLE([lexicon-output-path])
# ARG_OPTIONAL_SINGLE([max-epochs])
# ARG_OPTIONAL_SINGLE([encoding])
# ARG_HELP([<The general help message of my script>])
# ARGBASH_GO()
# needed because of Argbash --> m4_ignore([
### START OF CODE GENERATED BY Argbash v2.8.1 one line above ###
# Argbash is a bash code generator used to get arguments parsing right.
# Argbash is FREE SOFTWARE, see https://argbash.io for more info

die() {
    local _ret=$2
    test -n "$_ret" || _ret=1
    test "$_PRINT_HELP" = yes && print_help >&2
    echo "$1" >&2
    exit ${_ret}
}

begins_with_short_option() {
    local first_option all_short_options='h'
    first_option="${1:0:1}"
    test "$all_short_options" = "${all_short_options/$first_option/}" && return 1 || return 0
}

# THE DEFAULTS INITIALIZATION - OPTIONALS
#_arg_lang=
#_arg_lexicon_size=
#_arg_input_path=
#_arg_corpus_name=
#_arg_segmentation_output_path=
#_arg_model_output_path=
#_arg_lexicon_output_path=
_arg_seed_segmentation_input_path=
_arg_min_shift_remainder=1
_arg_length_threshold=5
_arg_perplexity_threshold=10
_arg_min_perplexity_length=1
_arg_max_epochs=5
_arg_encoding="utf-8"

print_help() {
    printf '%s\n' "Script for training LMVR"
    printf 'Usage: %s [--lang <arg>] [--lexicon-size <arg>] [--input-path <arg>] [--segmentation-output-path <arg>] [ --seed-segmentation-input-path <arg> ] [--model-output-path <arg>] [--min-shift-remainder <arg>] [--length-threshold <arg>] [--perplexity-threshold <arg>] [--min-perplexity-length <arg>] [--lexicon-output-path <arg>] [--max-epochs <arg>] [--encoding <arg>] [-h|--help]\n' "$0"
    printf '\t%s\n' "-h, --help: Prints help"
}

parse_commandline() {
    while test $# -gt 0; do
        _key="$1"
        case "$_key" in
        --lang)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_lang="$2"
            shift
            ;;
        --lang=*)
            _arg_lang="${_key##--lang=}"
            ;;
        --lexicon-size)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_lexicon_size="$2"
            shift
            ;;
        --lexicon-size=*)
            _arg_lexicon_size="${_key##--lexicon-size=}"
            ;;
        --input-path)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_input_path="$2"
            shift
            ;;
        --input-path=*)
            _arg_input_path="${_key##--input-path=}"
            ;;
        --corpus-name)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_corpus_name="$2"
            shift
            ;;
        --corpus-name=*)
            _arg_corpus_name="${_key##--corpus-name=}"
            ;;
        --segmentation-output-path)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_segmentation_output_path="$2"
            shift
            ;;
        --segmentation-output-path=*)
            _arg_segmentation_output_path="${_key##--segmentation-output-path=}"
            ;;
        --seed-segmentation-input-path)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_seed_segmentation_input_path="$2"
            shift
            ;;
        --seed-segmentation-input-path=*)
            _arg_seed_segmentation_input_path="${_key##--seed-segmentation-input-path=}"
            ;;
        --model-output-path)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_model_output_path="$2"
            shift
            ;;
        --model-output-path=*)
            _arg_model_output_path="${_key##--model-output-path=}"
            ;;
        --min-shift-remainder)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_min_shift_remainder="$2"
            shift
            ;;
        --min-shift-remainder=*)
            _arg_min_shift_remainder="${_key##--min-shift-remainder=}"
            ;;
        --length-threshold)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_length_threshold="$2"
            shift
            ;;
        --length-threshold=*)
            _arg_length_threshold="${_key##--length-threshold=}"
            ;;
        --perplexity-threshold)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_perplexity_threshold="$2"
            shift
            ;;
        --perplexity-threshold=*)
            _arg_perplexity_threshold="${_key##--perplexity-threshold=}"
            ;;
        --min-perplexity-length)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_min_perplexity_length="$2"
            shift
            ;;
        --min-perplexity-length=*)
            _arg_min_perplexity_length="${_key##--min-perplexity-length=}"
            ;;
        --lexicon-output-path)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_lexicon_output_path="$2"
            shift
            ;;
        --lexicon-output-path=*)
            _arg_lexicon_output_path="${_key##--lexicon-output-path=}"
            ;;
        --max-epochs)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_max_epochs="$2"
            shift
            ;;
        --max-epochs=*)
            _arg_max_epochs="${_key##--max-epochs=}"
            ;;
        --encoding)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_encoding="$2"
            shift
            ;;
        --encoding=*)
            _arg_encoding="${_key##--encoding=}"
            ;;
        -h | --help)
            print_help
            exit 0
            ;;
        -h*)
            print_help
            exit 0
            ;;
        *)
            _PRINT_HELP=yes die "FATAL ERROR: Got an unexpected argument '$1'" 1
            ;;
        esac
        shift
    done
}

parse_commandline "$@"

# OTHER STUFF GENERATED BY Argbash

### END OF CODE GENERATED BY Argbash (sortof) ### ])
# [ <-- needed because of Argbash

# get necessary environment variable and activate
# the virtual environment that uses python 2.7.
ROOT=$(dirname "$0")
if [ -z "$LMVR_ENV_PATH" ]; then
    source "$ROOT/lmvr-environment-variables.sh"
fi
source "$LMVR_ENV_PATH/bin/activate"

printf 'Value of --%s: %s\n' 'lang' "$_arg_lang"
printf 'Value of --%s: %s\n' 'lexicon-size' "$_arg_lexicon_size"
printf 'Value of --%s: %s\n' 'input-path' "$_arg_input_path"
printf 'Value of --%s: %s\n' 'corpus-name' "$_arg_corpus_name"
printf 'Value of --%s: %s\n' 'segmentation-output-path' "$_arg_segmentation_output_path"
printf 'Value of --%s: %s\n' 'seed-segmentation-input-path' "$_arg_seed_segmentation_input_path"
printf 'Value of --%s: %s\n' 'model-output-path' "$_arg_model_output_path"
printf 'Value of --%s: %s\n' 'min-shift-remainder' "$_arg_min_shift_remainder"
printf 'Value of --%s: %s\n' 'length-threshold' "$_arg_length_threshold"
printf 'Value of --%s: %s\n' 'perplexity-threshold' "$_arg_perplexity_threshold"
printf 'Value of --%s: %s\n' 'min-perplexity-length' "$_arg_min_perplexity_length"
printf 'Value of --%s: %s\n' 'lexicon-output-path' "$_arg_lexicon_output_path"
printf 'Value of --%s: %s\n' 'max-epochs' "$_arg_max_epochs"
printf 'Value of --%s: %s\n' 'encoding' "$_arg_encoding"

echo "Training morfessor baseline..."
corpusweight=1.0
MBL_SEGM_OUTPUT="$_arg_segmentation_output_path/morfessor-baseline-cw15.0.lmvr.${_arg_lexicon_size}.seed.${_arg_lang}"
MBL_LEXICON_OUTPUT_FNAME="${_arg_lexicon_output_path}/${_arg_corpus_name}.${_arg_lexicon_size}.morfessor-baseline-cw${corpusweight}.lexicon.${_arg_lang}.txt"

morfessor-train \
    -x ${MBL_LEXICON_OUTPUT_FNAME} \
    -S "${MBL_SEGM_OUTPUT}" \
    --max-epochs ${_arg_max_epochs} \
    --corpusweight "${corpusweight}" \
    "${_arg_input_path}"
SEED_SEGM_FNAME="${MBL_SEGM_OUTPUT}"

## Train LMVR model using the training set
echo "Training LMVR model..."
LMVR_MODEL_OUTPUT_FNAME="${_arg_model_output_path}/${_arg_corpus_name}.${_arg_lexicon_size}.lmvr-tuned.model.${_arg_lang}.tar.gz"
LMVR_LEXICON_OUTPUT_FNAME="${_arg_lexicon_output_path}/${_arg_corpus_name}.${_arg_lexicon_size}.lmvr-tuned.lexicon.${_arg_lang}.txt"

# TODO: why is -T relevant if we use lmvr-segment already?
lmvr-train "${SEED_SEGM_FNAME}" \
    -T "${_arg_input_path}" \
    -s "${LMVR_MODEL_OUTPUT_FNAME}" \
    -p "${_arg_perplexity_threshold}" \
    -d none -m batch \
    --min-shift-remainder "${_arg_min_shift_remainder}" \
    --length-threshold "${_arg_length_threshold}" \
    --min-perplexity-length "${_arg_min_perplexity_length}" \
    --max-epochs "${_arg_max_epochs}" \
    --lexicon-size "${_arg_lexicon_size}" \
    -x "${LMVR_LEXICON_OUTPUT_FNAME}" \
    -o /dev/null

# let's output the test to /dev/null
# since we're using lmvr-segment below

echo "Segmenting using LMVR..."
LMVR_SEGM_OUTPUT_FNAME="$_arg_segmentation_output_path/${_arg_corpus_name}.${_arg_lexicon_size}.segmented.lmvr-tuned.${_arg_lang}"
lmvr-segment \
    "${LMVR_MODEL_OUTPUT_FNAME}" \
    "${_arg_input_path}" \
    -p "${_arg_perplexity_threshold}" \
    --output-newlines \
    --encoding "${_arg_encoding}" \
    -o "${LMVR_SEGM_OUTPUT_FNAME}"

# ] <-- needed because of Argbash
