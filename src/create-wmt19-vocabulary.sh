#!/bin/bash

set -euxo pipefail

# Created by argbash-init v2.8.1
# ARG_OPTIONAL_SINGLE([lang])
# ARG_OPTIONAL_SINGLE([raw-data-folder])
# ARG_OPTIONAL_SINGLE([output-file])
# ARG_OPTIONAL_BOOLEAN([with-counts])
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
_arg_raw_data_folder=
_arg_output_file=
_arg_with_counts=

print_help() {
    printf '%s\n' "Script to generate vocabulary of input text, optionally with counts."
    printf 'Usage: %s [--lang <arg>] [--raw-data-folder <arg>] [--output-file <arg>] [--with-counts <arg>] [-h|--help]\n' "$0"
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
        --raw-data-folder)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_raw_data_folder="$2"
            shift
            ;;
        --raw-data-folder=*)
            _arg_raw_data_folder="${_key##--raw-data-folder=}"
            ;;
        --output-file)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_output_file="$2"
            shift
            ;;
        --output-file=*)
            _arg_output_file="${_key##--output-file=}"
            ;;
        --no-with-counts | --with-counts)
            _arg_with_counts="on"
            test "${1:0:5}" = "--no-" && _arg_with_counts="off"
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

#SCRIPTS=$(pwd)/src

if [ -z "${MOSES_SCRIPTS}" ]; then
    echo "Please make sure the MOSES_SCRIPTS environment variable is set!"
    exit 1
fi

MOSES_TOKENIZER_SCRIPT="$MOSES_SCRIPTS/tokenizer/tokenizer.perl"
MOSES_LOWERCASE_SCRIPT="$MOSES_SCRIPTS/tokenizer/lowercase.perl"
MOSES_NORM_PUNC="$MOSES_SCRIPTS/tokenizer/normalize-punctuation.perl"
MOSES_REM_NON_PRINT_CHAR="$MOSES_SCRIPTS/tokenizer/remove-non-printing-char.perl"

compute_token_counts() {
    LANGUAGE=$1
    WITH_COUNTS=$2

    if [ -n "$WITH_COUNTS" ]; then
        UNIQ_CMD="uniq -c"
        SORT_CMD="sort -nr"
    else
        UNIQ_CMD="uniq"
        SORT_CMD="sort"
    fi

    #if [ "$LANGUAGE" == "en" ]; then
    sed "s/--/ -- /g" |
        sed "s/[\/\\]/ /g" |
        perl "$MOSES_NORM_PUNC" "$LANGUAGE" |
        perl "$MOSES_REM_NON_PRINT_CHAR" |
        perl "$MOSES_TOKENIZER_SCRIPT" |
        perl "$MOSES_LOWERCASE_SCRIPT" |
        perl -C -MHTML::Entities -pe 'decode_entities($_);' |
        sed "s/ /\n/g" |
        sort |
        $UNIQ_CMD |
        sed "/^\s*/d" |
        $SORT_CMD
    #else
        #sed "s/--/ -- /g" |
            #sed "s/[\/\\]/ /g" |
            #sed "s/ /\n/g" |
            #sort |
            #$UNIQ_CMD |
            #sed "/^\s*/d" |
            #$SORT_CMD
    #fi
}

TRAIN_FILES="${_arg_raw_data_folder}/flores/*/train.${_arg_lang}"
TRAIN_FILES="${TRAIN_FILES//\\n/ }" 

if [ "$_arg_lang" = "kk" ]; then
    lang="ru"
else
    lang="$_arg_lang"
fi

if [ -z "$_arg_output_file" ]; then

    # if no output file provided, just pipe to stdout
    cat ${TRAIN_FILES} |
        compute_token_counts "$lang" "$_arg_with_counts"
else

    # otherwise, save in output file
    cat ${TRAIN_FILES} |
        compute_token_counts "$lang" "$_arg_with_counts" \
            >"${_arg_output_file}"
fi

# ] <-- needed because of Argbash
