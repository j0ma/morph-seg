import pandas as pd
import click
import os
import re

def grab(s):
    try:
        pieces = re.findall("\(\((.*)\),", s)[0].replace("'", "").split(', ')
        return " ".join(pieces)
    except:
        return s

@click.command()
@click.option('--slug', required=True)
@click.option('--output-filename', required=True)
@click.option('--segmentation-folder', default='../data/segmented/', required=False)
@click.option('--raw-data-folder', default='../data/raw/', required=False)
@click.option('--output-folder', default='../data', required=False)
def main(segmentation_folder, raw_data_folder, output_folder, output_filename, slug):

    INPUT_FOLDER = os.path.abspath(segmentation_folder)
    RAW_INPUT_FOLDER = os.path.abspath(raw_data_folder + slug)
    OUTPUT_FOLDER = os.path.abspath(output_folder)
    OUTPUT_FNAME = output_filename

    with open(os.path.abspath(RAW_INPUT_FOLDER), 'r') as f:
        WORDS = [w.strip() for w in f.readlines()]

    BASELINE_SUFFIXES =[
        ".segmented.morfessor-baseline-batch-recursive",
        ".segmented.morfessor-baseline-batch-viterbi",
        ".segmented.morfessor-baseline-online-recursive",
        ".segmented.morfessor-baseline-online-viterbi",
        ".segmented.flatcat-batch"
    ]

    BASELINE_FILENAMES = [slug + suff for suff in BASELINE_SUFFIXES]

    BPE_SUFFIXES = [
        ".segmented.sentencepiece",
        ".segmented.subword-nmt"
    ]

    BPE_FILENAMES = [slug + suff for suff in BPE_SUFFIXES]

    FILENAMES = [fn for fn in BASELINE_FILENAMES+BPE_FILENAMES if fn!=""]
    FILENAMES = [os.path.join(INPUT_FOLDER, f) for f in FILENAMES]
    IS_BPE = [False]*len(BASELINE_FILENAMES) + [True]*len(BPE_FILENAMES)

    NAMES = [
        suff.replace('.segmented.', '').replace('morfessor-', '')
        for suff in BASELINE_SUFFIXES + BPE_SUFFIXES
    ]

    output = pd.DataFrame()
    output['word'] = WORDS

    for fn, is_bpe, name in zip(FILENAMES, IS_BPE, NAMES):
        if is_bpe:
            segm = [w.rstrip() for w in open(fn, 'r')]
        else:
            lines = [w.strip() for w in open(fn, 'r')]
            segm = [l.split('\t')[1] for l in lines]
            if 'flatcat' in name:
                segm = [grab(s) for s in segm]

        output[name] = segm

    # Shuffle the data
    output = output.sample(frac=1).reset_index(drop=True)

    MARKDOWN_TABLE_PATH = os.path.join(OUTPUT_FOLDER, OUTPUT_FNAME)
    PKL_PATH = MARKDOWN_TABLE_PATH.replace('.md', '.pkl')
    with open(MARKDOWN_TABLE_PATH, 'w') as MARKDOWN_TABLE_FILE:
        output.to_markdown(MARKDOWN_TABLE_FILE)

    output.to_pickle(PKL_PATH)

if __name__ == '__main__':
    main()
