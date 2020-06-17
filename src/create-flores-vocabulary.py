"""
create-flores-vocab.py

reads in all the training files used to train flores,
and extracts their english vocabularies
"""

from collections import Counter
import sacremoses as sm
import itertools as it
import helpers as h
import pickle
import click
import math
import os

@click.command()
@click.option('--lang', required=True)
@click.option('--output-file', '-o')
@click.option('--dry-run', is_flag=True, default=False)
@click.option('--with-counts', is_flag=True, default=False)
def main(lang, output_file=None, dry_run=False, with_counts=False):

    if output_file is None:
        output_file = f'all-flores-words-{lang}'

    if lang == 'en':
        data_folders = ["../data/raw/wiki_ne_en", "../data/raw/wiki_si_en"]
        OUTPUT_PATH = os.path.join('../data/raw/', output_file)
    else:        
        data_folders = [f"../data/raw/wiki_{lang}_en"]
        OUTPUT_PATH = os.path.join(data_folders[0], output_file)

    PATHS= [f"{df}/train.{lang}" for df in data_folders]

    # instantiate tokenizer
    if lang == 'en':
        tokenize = lambda sent: sm.MosesTokenizer('en').tokenize(sent)
    else:
        # we don't need to tokenize since indic_nlp_library already did
        tokenize = lambda sent: sent.split() 

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

    def all_sentences(paths, n_max=None):
        sents = flatten([read_file(p) for p in paths])
        if n_max is not None:
            for s, i in zip(sents, range(n_max)):
                yield s
        else:
            for s in sents:
                    yield s

    def all_tokens(sentences):
        for t in flatten([tokenize(sent) for sent in sentences]):
            yield t

    N_MAX = None
    ALL_TOKEN_COUNTS = Counter(t for t in all_tokens(all_sentences(PATHS, n_max=N_MAX)) if is_word(t))
    ALL_LOWERCASE_TOKEN_COUNTS = Counter(t.lower() for t in all_tokens(all_sentences(PATHS, n_max=N_MAX)) if is_word(t))

    n_types_non_lowercase = len(ALL_TOKEN_COUNTS)
    n_types_lowercase = len(ALL_LOWERCASE_TOKEN_COUNTS)
    print(f"No. of word types (non-lowercased): {n_types_non_lowercase}")
    print(f"No. of word types (lowercased): {n_types_lowercase}")
    print(f"Data compression ratio: {round(n_types_non_lowercase/n_types_lowercase, 3)}")

    if not dry_run:

        # create output files
        ALL_WORD_TOKENS_WITHCOUNTS = list(reversed(sorted(ALL_TOKEN_COUNTS.items(), key=lambda t: t[1])))
        ALL_WORD_TOKENS_NOCOUNTS = [t for t, c in ALL_WORD_TOKENS_WITHCOUNTS]

        ALL_LOWERCASE_WORD_TOKENS_WITHCOUNTS = list(reversed(sorted(ALL_LOWERCASE_TOKEN_COUNTS.items(), key=lambda t: t[1])))
        ALL_LOWERCASE_WORD_TOKENS_NOCOUNTS = [t for t, c in ALL_LOWERCASE_WORD_TOKENS_WITHCOUNTS]

        h.write_file(ALL_WORD_TOKENS_NOCOUNTS, OUTPUT_PATH)
        h.write_file(ALL_LOWERCASE_WORD_TOKENS_NOCOUNTS, 
                     OUTPUT_PATH + '-lowercase')

        if with_counts:
            ALL_WORD_TOKENS_WITHCOUNTS = [f"{c}\t{t}" for t,c in ALL_WORD_TOKENS_WITHCOUNTS]
            ALL_LOWERCASE_WORD_TOKENS_WITHCOUNTS = [f"{c}\t{t}" for t,c in ALL_LOWERCASE_WORD_TOKENS_WITHCOUNTS]
            h.write_file(ALL_WORD_TOKENS_WITHCOUNTS, OUTPUT_PATH + '-withcounts')
            h.write_file(ALL_LOWERCASE_WORD_TOKENS_WITHCOUNTS, 
                         OUTPUT_PATH + '-lowercase-withcounts')

if __name__ == '__main__':
    main()
