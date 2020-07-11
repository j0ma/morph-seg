#!/bin/bash

A=$1
B=$2
FNAME_A="/tmp/$(basename "${A}")"
FNAME_B="/tmp/$(basename "${B}")"
DIFF="vimdiff"
#DIFF="gdiff"

# function to get rid of empty lines,
# and then grab only every other line
grab_segmentations() {
    sed "/^\s*$/d" | awk "NR%2==0"
}

gdiff() {
    git diff --no-index --color-words "${1}" "${2}"
}

grab_segmentations <"${A}" >"${FNAME_A}"
grab_segmentations <"${B}" >"${FNAME_B}"

"${DIFF}" "${FNAME_A}" "${FNAME_B}"
rm -Rf "${FNAME_A}" "${FNAME_B}"
