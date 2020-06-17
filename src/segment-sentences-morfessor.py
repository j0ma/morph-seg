from collections import Counter
import sacremoses as sm
import itertools as it
import helpers as h
import morfessor
import flatcat
import pickle
import click
import os

def load_model(model_file):
    io = morfessor.MorfessorIO()
    model = io.read_binary_model_file(model_file)
    return model

@click.command()
@click.option('--input-file','-i', help="Path to load input from")
@click.option('--output-file','-o', help="Path to save output to")
@click.option('--model-file','-m', help="Path of model binary file")
@click.option('--include-original', is_flag=True, required=False, default=False)
@click.option('--lang', '-l', help="Language")
def main(input_file, output_file, model_file, include_original, lang):
    sentences = h.read_lines(input_file)
    model = load_model(model_file)
    if lang == 'en':
        tokenizer = sm.MosesTokenizer('en')
    else:
        tokenizer = None
    segmented = [
        h.segment_sentence(model, s, tokenizer)
        for s in sentences
    ]

    if include_original:
        segmented = [f"{sent}\t{segm}" for sent, segm in zip(sentences, segmented)]

    h.write_file(segmented, output_file)

if __name__ == '__main__':
    main()
