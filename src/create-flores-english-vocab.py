"""
create-flores-english-vocab.py

reads in all the training files used to train flores,
and extracts their english vocabularies
"""

import sacremoses as sm
import itertools as it
import pickle
import os

DATA_FOLDER = "../data/raw"
FILES = [f for f in os.listdir(DATA_FOLDER) if f.endswith('.en')]
PATHS = [os.path.join(DATA_FOLDER, f) for f in FILES]
OUTPUT_PATH = os.path.join(DATA_FOLDER, 'all-flores-words.en')

# instantiate tokenizer
tok = sm.MosesTokenizer('en')

# load the files
def read_file(p):
    with open(p, 'r') as f:
        for l in f:
            yield l.strip()

def flatten(nested):
    for x in it.chain.from_iterable(nested):
        yield x

def is_word(token):
    return (not token) or (token[0].isalnum())

ALL_SENTENCES = flatten([read_file(p) for p in PATHS])
ALL_TOKENS = flatten([tok.tokenize(sent) for sent in ALL_SENTENCES])
ALL_WORD_TOKENS = '\n'.join(sorted({t for t in ALL_TOKENS if is_word(t)}))

with open(OUTPUT_PATH, 'w') as f:
    f.write(ALL_WORD_TOKENS)

