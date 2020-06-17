"""
create-flores-vocab.py

reads in all the training files used to train flores,
and extracts their english vocabularies
"""

import sacremoses as sm
import itertools as it
import pickle
import click
import os

@click.command()
@click.option('--lang', required=True)
@click.option('--output-file', '-o')
def main(lang, output_file=None):

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

    ALL_SENTENCES = flatten([read_file(p) for p in PATHS])
    ALL_TOKENS = flatten([tokenize(sent) for sent in ALL_SENTENCES])
    ALL_WORD_TOKENS = '\n'.join(sorted({t for t in ALL_TOKENS if is_word(t)}))

    with open(OUTPUT_PATH, 'w') as f:
        f.write(ALL_WORD_TOKENS)

if __name__ == '__main__':
    main()
