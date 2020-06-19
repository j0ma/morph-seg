"""
create-flores-vocab.py

reads in all the training files used to train flores,
and extracts their english vocabularies
"""

import itertools as it
import math
import os
import string
from collections import Counter

import click
import sacremoses as sm

PUNC = set(string.punctuation)


def read_file(p):
    with open(p, "r") as f:
        for line in f:
            yield line.strip()


def flatten(nested):
    for x in it.chain.from_iterable(nested):
        yield x


def is_word(token):
    return (not token) or token in PUNC or (token[0].isalnum())


def compute_token_counts(paths, tokenize=None, n_max=None):
    """Computes token counts"""
    n_iters = 0

    if n_max is None:
        n_max = math.inf

    token_counts = Counter()
    lowercase_token_counts = Counter()

    for path in paths:
        sentences = read_file(path)

        for sent in sentences:
            n_iters += 1

            if n_iters >= n_max:
                return token_counts, lowercase_token_counts

            tokens = tokenize(sent)

            for t in tokens:
                if not is_word(t):
                    continue
                token_counts[t] += 1
                lowercase_token_counts[t.lower()] += 1

    return token_counts, lowercase_token_counts


def dump_tokens(
    token_counts, output_path, output_path_with_counts, with_counts
):
    with open(output_path, "w") as f_no_counts, open(
        output_path_with_counts, "w"
    ) as f_with_counts:
        for token, token_count in reversed(
            sorted(token_counts.items(), key=lambda t: t[1])
        ):
            f_no_counts.write(f"{token}\n")

            if with_counts:
                f_with_counts.write(f"{token_count}\t{token}\n")


@click.command()
@click.option("--lang", required=True)
@click.option("--output-file", "-o")
@click.option("--dry-run", is_flag=True, default=False)
@click.option("--with-counts", is_flag=True, default=False)
@click.option("--n-max", type=int)
def main(lang, output_file=None, dry_run=False, with_counts=False, n_max=None):

    if output_file is None:
        output_file = f"flores.vocab.{lang}"

    if lang == "en":
        data_folders = ["../data/raw/wiki_ne_en", "../data/raw/wiki_si_en"]
        output_path = os.path.join("../data/raw/", output_file)
    else:
        data_folders = [f"../data/raw/wiki_{lang}_en"]
        output_path = os.path.join(data_folders[0], output_file)

    input_paths = [f"{df}/train.{lang}" for df in data_folders]
    output_path_with_counts = output_path + ".withcounts"
    output_path_lowercase = output_path + ".lowercase"
    output_path_lowercase_with_counts = output_path + ".lowercase.withcounts"

    # instantiate tokenizer

    if lang == "en":

        def tokenize(sent):
            return sm.MosesTokenizer("en").tokenize(sent)

    else:
        # we don't need to tokenize since indic_nlp_library already did in prepare_{ne,si}en.sh
        def tokenize(sent):
            return sent.split(" ")

    # load the files
    token_counts, lowercase_token_counts = compute_token_counts(
        input_paths, tokenize, n_max
    )
    n_types_non_lowercase = len(token_counts)
    n_types_lowercase = len(lowercase_token_counts)
    compression_ratio = round(n_types_non_lowercase / n_types_lowercase, 3)
    print(f"No. of word types (non-lowercased): {n_types_non_lowercase}")
    print(f"No. of word types (lowercased): {n_types_lowercase}")
    print(f"Data compression ratio: {compression_ratio}")

    if not dry_run:

        dump_tokens(
            token_counts, output_path, output_path_with_counts, with_counts
        )

        dump_tokens(
            lowercase_token_counts,
            output_path_lowercase,
            output_path_lowercase_with_counts,
            with_counts,
        )


if __name__ == "__main__":
    main()
