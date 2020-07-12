from collections import defaultdict
import click

TAB = "\t"
SPACE = " "
NEWLINE = "\n"


def read_sentences(sentences_path):
    sentences = [
        line.strip()

        for line in open(sentences_path, "r")

        if line.strip() != ""
    ]

    return sentences


def read_segmentations(segmentations_path):
    with open(segmentations_path, "r") as f:
        out = defaultdict(str)

        for line in f.readlines():
            if not line.strip():
                continue
            try:
                parts = line.strip().split(SPACE)
                w, segm = parts[0], " ".join(parts[1:])
            except ValueError:
                print(line)
                raise ValueError(line)
            out[w] = segm

        return out


@click.command()
@click.option("--sentences")
@click.option("--segmentations")
@click.option("--output")
def main(sentences, segmentations, output):
    # step 0: read in sentences
    sentences = read_sentences(sentences)

    # step 1: read segmentation file and create mapping
    print("Reading in word -> segmentation map...")
    segmentations = read_segmentations(segmentations)

    # step 2: loop over sentences and create segmentations
    print("Segmenting sentences...")
    segmented_sentences = []

    for sent in sentences:
        print("Sentence: {}".format(sent))
        tokens_out = []

        for token in sent.split(SPACE):
            tokens_out.append(segmentations[token])
        sent_out = SPACE.join(tokens_out)
        segmented_sentences.append(sent_out)

    # step 3: write corpus to output
    print("Writing output to disk...")
    segmented_corpus = NEWLINE.join(segmented_sentences)
    with open(output, "w") as f:
        f.write(segmented_corpus)


if __name__ == "__main__":
    main()
