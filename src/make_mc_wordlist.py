#! /usr/bin/env python

"""
Make a Morpho Challenge (MC) format wordlist from space-delimited tokens.

Reads from stdin and write to stdout.
"""


import sys
from collections import Counter

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

word_counts = Counter()

for line in sys.stdin:
    words = line.strip().split(" ")
    for word in words:
        word = word.strip().lower()
        if word:
            word_counts[word] += 1

for word, count in word_counts.most_common():
    print(count, word)
