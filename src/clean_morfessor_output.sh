#!/usr/bin/env bash
set -euo pipefail

tail -n +2 |  # Skip the comment line
  cut -d " " -f 2- |  # Remove the count
  sed 's/ + / /g' |  # Replace " + " with " "
  awk '{w=$0; gsub(" ", "", w); print w, $0}' OFS='\t'  # Add the original form word before a tab and the analysis
