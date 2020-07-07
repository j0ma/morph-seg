#! /usr/bin/env python

"""
Convert a Morpho Challenge wordlist into a dict for subword-nmt.

Reads from stdin and writes to stdout.
"""

import sys

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

for line_num, line in enumerate(sys.stdin, 1):
    fields = line.rstrip("\n").split(" ")
    if len(fields) != 2:
        raise ValueError(f"Line {line_num} is not properly formatted: {repr(line)}")
    count, word = fields
    if not word.strip():
        print(f"Skipping whitespace word of length {len(word)} on line {line_num}: {repr(line)}", file=sys.stderr)
        continue

    # Original format is (count, word), output is (word, count)
    print(word, count)
