import click
import sys

TAB = "\t"
SPACE = " "
NEWLINE = "\n"


def read_sentences(sentences_path):
    sentences = [line.strip() for line in open(sentences_path, "r")]

    return sentences


def read_segmentations(segmentations_path):
    with open(segmentations_path, "r") as f:
        out = {}

        for line in f.readlines():
            try:
                parts = line.strip().split(SPACE)
                w, segm = parts[0], " ".join(parts[1:])
            except ValueError:
                raise ValueError(line)
            out[w] = segm

        return out

def segment(w, segm_map):
    try:
        return segm_map[w]
    except KeyError:
        return w

@click.command()
@click.option("--sentences")
@click.option("--segmentations")
@click.option("--output")
def main(sentences, segmentations, output):
    # step 0: read in sentences
    sentences = read_sentences(sentences)

    # step 1: read segmentation file and create mapping
    sys.stderr.write("Reading in word -> segmentation map...\n")
    segmentations = read_segmentations(segmentations)

    # step 2: loop over sentences and create segmentations
    sys.stderr.write("Segmenting sentences...\n")
    segmented_sentences = []

    for sent in sentences:
        tokens_out = []

        for token in sent.split(SPACE):
            tokens_out.append(segment(token, segm_map=segmentations))
        sent_out = SPACE.join(tokens_out)
        segmented_sentences.append(sent_out)

    assert len(sentences) == len(segmented_sentences)

    # step 3: write corpus to output
    sys.stderr.write("Writing output to disk...\n")
    # segmented_corpus = NEWLINE.join(segmented_sentences)
    # with open(output, "a") as f:
        # for segm_sent in segmented_sentences:
            # f.write(segm_sent)

    for segm_sent in segmented_sentences:
        sys.stdout.write(segm_sent+"\n")


if __name__ == "__main__":
    main()
