import pandas as pd
import os

INPUT_FOLDER = os.path.abspath('../data/segmented/')
OUTPUT_FOLDER = os.path.abspath('../data/')
OUTPUT_FNAME='comparison-table-yiddish.md'

with open(os.path.abspath('../data/raw/yiddish-lrec2020-romanized'), 'r') as f:
    WORDS = [w.strip() for w in f.readlines()]

BASELINE_FILENAMES = """
yiddish-lrec2020-romanized.segmented.morfessor-baseline-batch-recursive
yiddish-lrec2020-romanized.segmented.morfessor-baseline-batch-viterbi
yiddish-lrec2020-romanized.segmented.morfessor-baseline-online-recursive
yiddish-lrec2020-romanized.segmented.morfessor-baseline-online-viterbi
yiddish-lrec2020-romanized.segmented.flatcat-batch
""".split('\n')[1:]

BPE_FILENAMES = """
yiddish-lrec2020-romanized.segmented.sentencepiece
yiddish-lrec2020-romanized.segmented.subword-nmt
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
# n_spaces = output.applymap(lambda s: sum([1 if ' ' in c else 0 for c in s])).sum(axis=1)
# output['n_spaces'] = n_spaces
# output.sort_values('n_spaces', ascending=False, inplace=True)

# Shuffle the data
output = output.sample(frac=1).reset_index(drop=True)

MARKDOWN_TABLE_PATH = os.path.join(OUTPUT_FOLDER, OUTPUT_FNAME)
PKL_PATH = MARKDOWN_TABLE_PATH.replace('.md', '.pkl')
with open(MARKDOWN_TABLE_PATH, 'w') as MARKDOWN_TABLE_FILE:
    output.to_markdown(MARKDOWN_TABLE_FILE)

output.to_pickle(PKL_PATH)

    






