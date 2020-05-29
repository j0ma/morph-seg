import pandas as pd
import os

INPUT_FOLDER = os.path.abspath('../data/segmented/')
OUTPUT_FOLDER = os.path.abspath('../data/')
OUTPUT_FNAME='comparison-table-flores.md'

with open(os.path.abspath('../data/raw/all-flores-words-nonumbers.en'), 'r') as f:
    WORDS = [w.strip() for w in f.readlines()]

BASELINE_FILENAMES = """
all-flores-words-nonumbers.segmented.morfessor-baseline-batch-recursive.en
all-flores-words-nonumbers.segmented.morfessor-baseline-batch-viterbi.en
all-flores-words-nonumbers.segmented.morfessor-baseline-online-recursive.en
all-flores-words-nonumbers.segmented.morfessor-baseline-online-viterbi.en
all-flores-words-nonumbers.segmented.flatcat-batch.en
""".split('\n')[1:]

BPE_FILENAMES = """
all-flores-words-nonumbers.en.segmented.sentencepiece
all-flores-words-nonumbers.en.segmented.subword-nmt
""".split('\n')[1:]

FILENAMES = [fn for fn in BASELINE_FILENAMES+BPE_FILENAMES if fn!=""]

FILENAMES = [os.path.join(INPUT_FOLDER, f) for f in FILENAMES]
IS_BPE = [False, False, False, False, False, True, True]
NAMES = ['baseline-batch-recursive', 'baseline-batch-viterbi',
         'baseline-online-recursive', 'baseline-online-viterbi',
         'sentencepiece', 'subword-nmt']

output = pd.DataFrame()
output['word'] = WORDS

for fn, is_bpe, name in zip(FILENAMES, IS_BPE, NAMES):

    if is_bpe:
        segm = [w.rstrip() for w in open(fn, 'r')]
    else:
        lines = [w.strip() for w in open(fn, 'r')]
        segm = [l.split('\t')[1] for l in lines]

    output[name] = segm

# sort by total number of spaces in row (to show segmented words)
n_spaces = output.applymap(lambda s: sum([1 if ' ' in c else 0 for c in s])).sum(axis=1)
output['n_spaces'] = n_spaces
output.sort_values('n_spaces', ascending=False, inplace=True)

with open(os.path.join(OUTPUT_FOLDER, OUTPUT_FNAME), 'w') as MARKDOWN_TABLE_PATH:
    output.to_markdown(MARKDOWN_TABLE_PATH)

    






