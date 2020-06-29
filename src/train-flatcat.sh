#!/bin/bash

# Created by argbash-init v2.8.1
# ARG_OPTIONAL_SINGLE([lang])
# ARG_OPTIONAL_SINGLE([model-type])
# ARG_OPTIONAL_SINGLE([model-output-path])
# ARG_OPTIONAL_SINGLE([construction-separator])
# ARG_OPTIONAL_SINGLE([perplexity-threshold])
# ARG_OPTIONAL_BOOLEAN([lowercase])
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
_arg_lang=
_arg_model_type=
_arg_model_output_path=
_arg_construction_separator=" + "
_arg_perplexity_threshold=
_arg_lowercase="off"

print_help() {
    printf '%s\n' "Perform FlatCat training seeded by Baseline segmentations"
    printf 'Usage: %s [--lang <arg>] [--model-type <arg>] [--model-output-path <arg>] [--construction-separator <arg>] [--perplexity-threshold <arg>] [--(no-)lowercase] [-h|--help]\n' "$0"
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
        --model-type)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_model_type="$2"
            shift
            ;;
        --model-type=*)
            _arg_model_type="${_key##--model-type=}"
            ;;
        --model-output-path)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_model_output_path="$2"
            shift
            ;;
        --model-output-path=*)
            _arg_model_output_path="${_key##--model-output-path=}"
            ;;
        --construction-separator)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_construction_separator="$2"
            shift
            ;;
        --construction-separator=*)
            _arg_construction_separator="${_key##--construction-separator=}"
            ;;
        --perplexity-threshold)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_perplexity_threshold="$2"
            shift
            ;;
        --perplexity-threshold=*)
            _arg_perplexity_threshold="${_key##--perplexity-threshold=}"
            ;;
        --no-lowercase | --lowercase)
            _arg_lowercase="on"
            test "${1:0:5}" = "--no-" && _arg_lowercase="off"
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

if [ "$_arg_lowercase" == "off" ]; then
    SEED_SEGMENTATION="flores.vocab.${_arg_lang}.segmented.morfessor-baseline-batch-recursive"
else
    SEED_SEGMENTATION="flores.vocab.${_arg_lang}.lowercase.segmented.morfessor-baseline-batch-recursive"
fi

SEED_PATH="./data/segmented/flores/${_arg_lang}/${SEED_SEGMENTATION}"

# PARAMS TO TUNE: (TODO!)
# - p: perplexity threshold
# - w: corpus weight
# - W: annotation weight

# Perform training

echo "Model type: ${_arg_model_type}"
echo "Model output path: ${_arg_model_output_path}"
echo "Construction sep: ${_arg_construction_separator}"
echo "Perplexity thres: ${_arg_perplexity_threshold}"
echo "Language: ${_arg_lang}"

MODEL_OUTPUT_PATH="${_arg_model_output_path}/flores.vocab.${_arg_lang}.lowercase-morfessor-flatcat-${_arg_model_type}-${_arg_lang}.bin"

flatcat-train \
    "$SEED_PATH" \
    -m "$_arg_model_type" \
    --save-binary-model "$MODEL_OUTPUT_PATH" \
    --construction-separator "$_arg_construction_separator" \
    --category-separator "ThisWontThrowError" \
    --perplexity-threshold "$_arg_perplexity_threshold" \
    --progressbar -e "UTF-8"

#flatcat-segment \
    #"$SEED_PATH" \
    #-m "$_arg_model_type" \
    #--save-binary-model "$MODEL_OUTPUT_PATH" \
    #--construction-separator "$_arg_construction_separator" \
    #--category-separator "ThisWontThrowError" \
    #--perplexity-threshold "$_arg_perplexity_threshold" \
    #--progressbar -e "UTF-8"
# ] <-- needed because of Argbash
