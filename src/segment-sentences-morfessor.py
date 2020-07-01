# -*- coding: utf-8 -*-
import itertools as it
import os
import pickle
from collections import Counter

import click
import flatcat
import morfessor
# import sacremoses as sm

import helpers as h


def load_model(model_file):

    # tarball only used for LMVR
    if model_file.endswith('tar.gz'):
        io = flatcat.FlatcatIO()
        model = io.read_tarball_model_file(model_file)
        model.initialize_hmm()

    else:
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
@click.option("--lowercase", is_flag=True, default=False)
@click.option("--tokenize", is_flag=True, default=False, help="Tokenize with Sacremoses")
@click.option("--lang", "-l", help="Language")
@click.option("--print-every", default=1000)
def main(
    input_file, output_file, model_file, include_original, lowercase, tokenize, lang, print_every=100
):
    sentences = h.read_lines(input_file)
    model = load_model(model_file)

    # NOTE: DEPRECATED
    # we only tokenize if the language is english and the user explicitly requested it
    # if lang == "en" and tokenize:
        # print('Tokenizing using Sacremoses!')
        # tokenizer = sm.MosesTokenizer("en")
    # elif tokenize:
        # raise NotImplementedError("Only EN tokenization supported with Moses!")
    # else:
        # tokenizer = None

    # disable sacremoses
    tokenizer = None

    segmented = []

    n_sent = len(sentences)
    for ix, s in enumerate(sentences):
        if ix % print_every == 0:
            print('Processing sentence {}/{}'.format(ix+1, n_sent))

        if lowercase:
            s = s.lower()
        seg = h.segment_sentence(model, s, tokenizer)
        segmented.append(seg)

    if include_original:
        segmented = [
            "{}\t{}".format(sent, segm) 
            for sent, segm 
            in zip(sentences, segmented)
        ]

    if output_file != "-":
        h.write_file(segmented, output_file)
    else:
        for s in segmented:
            sys.stdout.write("{}\n".format(s))


if __name__ == "__main__":
    main()
