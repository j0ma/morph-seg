import itertools as it
import os
import pickle
import sys
from collections import Counter

import click
import flatcat
import morfessor
import sacremoses as sm

import helpers as h


def load_model(model_file):
    io = morfessor.MorfessorIO()
    model = io.read_binary_model_file(model_file)

    return model


@click.command()
@click.option("--input-file", "-i", help="Path to load input from")
@click.option(
    "--output-file", "-o", help="Path to save output to", default="-"
)
@click.option("--model-file", "-m", help="Path of model binary file")
@click.option(
    "--include-original", is_flag=True, required=False, default=False
)
@click.option('--lowercase', is_flag=True, default=False)
@click.option("--lang", "-l", help="Language")
def main(input_file, output_file, model_file, include_original, lowercase, lang):
    sentences = h.read_lines(input_file)
    model = load_model(model_file)

    if lang == "en":
        tokenizer = sm.MosesTokenizer("en")
    else:
        tokenizer = None

    segmented = []

    for s in sentences:
        if lowercase:
            s = s.lower()
        seg = h.segment_sentence(model, s, tokenizer)
        segmented.append(seg)

    if include_original:
        segmented = [
            f"{sent}\t{segm}" for sent, segm in zip(sentences, segmented)
        ]

    if output_file != "-":
        h.write_file(segmented, output_file)
    else:
        for s in segmented:
            sys.stdout.write(f"{s}\n")


if __name__ == "__main__":
    main()
