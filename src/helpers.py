import itertools as it
import os
import pickle

import flatcat
import morfessor

UTF8 = "utf-8"


def segment_word(model, w):
    """
    Description
    -----------
    Segment word `w` using `model` by looking up w
    in the model analyses, and default to Viterbi
    segmentation if necessary, ie. in case `w` is OOV
    or in case the model does not support .segment().
    """
    try:
        out = model.segment(w)
    except (KeyError, AttributeError):
        out = model.viterbi_segment(w)[0]

    return out


def segment_sentence(model, sentence, tokenizer=None):
    """
    Description
    -----------
    Segments `sentence` using `model` and `tokenizer`.

    Parameters
    ----------
    model: Morfessor model
    sentence: str
    tokenizer: object
    """

    if tokenizer is not None:
        words = tokenizer.tokenize(sentence)
    else:
        words = sentence.split()

    segmentations = flatten([segment_word(model, w) for w in words])

    return " ".join(segmentations)


def train_model(
    lang,
    model_name,
    input_path,
    input_file_name,
    model_output_folder,
    model_output_path,
    segm_output_folder,
    corpus_weight=1.0,
    construction_separator=" + ",
    lowercase=True,
):
    """
    Description
    ------------
    Trains the Morfessor Baseline model.
    After training, dumps model binary to disk
    and performs segmentation on the training data.
    """

    if not model_output_folder or model_output_path:
        err_msg = (
            "Required: one of `model_output_folder` or `model_output_path`"
        )
        raise ValueError(err_msg)

    model = f"morfessor-{model_name}"
    output_filename = f"{input_file_name}.segmented.{model}"
    output_path = os.path.join(segm_output_folder, output_filename)

    print(f"Now running: {model}")

    if "flatcat" in model:

        def run(model_name, input_path):
            return run_morfessor_flatcat(
                model_name,
                input_path,
                construction_separator=construction_separator,
                lang=lang,
                lowercase=lowercase,
            )

    else:

        def run(model_name, input_path):
            return run_morfessor_baseline(
                model_name,
                input_path,
                construction_separator=construction_separator,
                lang=lang,
                lowercase=lowercase,
            )

    model_bin = run(model, input_path)

    # get segmenetations
    io = morfessor.MorfessorIO(
        encoding=UTF8, construction_separator=construction_separator
    )
    segmentations = model_bin.get_segmentations()

    if segmentations:
        io.write_segmentation_file(output_path, segmentations)
    else:
        print("No segmentations received, not going to write to disk...")

    # save model to pickle

    if model_bin is not None:
        bin_path = (
            model_output_path
            or f"{model_output_folder}/{input_file_name}-{model}-{lang}.bin"
        )
        io.write_binary_model_file(bin_path, model_bin)
    else:
        print("No model received, not going to write to disk...")


def run_morfessor_baseline(
    model_name,
    input_path,
    construction_separator=" ",
    hyperparams=None,
    lang=None,
    lowercase=True,
):
    if hyperparams is None:
        hyperparams = {}

    io = morfessor.MorfessorIO()
    train_data = [w for w in io.read_corpus_list_file(input_path)]

    training_type = model_name.replace("morfessor-baseline-", "")

    model = morfessor.BaselineModel()

    if training_type == "batch-recursive":
        model.load_data(train_data)
        model.train_batch()
    elif training_type == "batch-viterbi":
        model.load_data(train_data)
        model.train_batch(algorithm="viterbi")
    elif training_type == "online-recursive":
        model.train_online(data=(d for d in train_data))
    elif training_type == "online-viterbi":
        model.train_online(data=(d for d in train_data), algorithm="viterbi")
    else:
        raise ValueError("Invalid training method!")

    return model


def run_morfessor_flatcat(
    model_name,
    input_path,
    lang="en",
    seed_segmentation_path=None,
    construction_separator=" + ",
    corpus_weight=1.0,
    lowercase=True,
):

    # TODO: do these work?

    if seed_segmentation_path is None:
        if lowercase:
            _ = f"flores.vocab.{lang}.lowercase.segmented.morfessor-baseline-batch-recursive"
        else:
            _ = f"flores.vocab.{lang}.segmented.morfessor-baseline-batch-recursive"
        seed_segmentation_path = os.path.abspath(
            f"../data/segmented/flores/{lang}/{_}"
        )

    io = flatcat.FlatcatIO(construction_separator=construction_separator)

    train_data = [t for t in io.read_corpus_list_file(input_path)]

    # if lowercase:
    # train_data = [t.lower() for t in train_data]

    morph_usage = flatcat.categorizationscheme.MorphUsageProperties()
    model = flatcat.FlatcatModel(morph_usage, corpusweight=corpus_weight)

    seed_segmentation_file = [
        x for x in io.read_segmentation_file(seed_segmentation_path)
    ]

    print("adding seed segmentations")
    model.add_corpus_data(seed_segmentation_file)
    model.initialize_hmm()

    training_type = "online" if "online" in model_name else "batch"

    if training_type == "batch":
        model.train_batch()
    elif training_type == "online":
        model.train_online(data=(d for d in train_data))
    else:
        raise ValueError("Invalid training method!")

    return model


def dump_pickle(obj, f):
    with open(f, "wb") as fout:
        pickle.dump(obj, fout)


def write_file(lines, f, sep="\n"):
    with open(f, "w") as fout:
        fout.writelines([line + sep for line in lines])


def read_lines(f):
    with open(f, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip() != ""]


def flatten(nested):
    return list(it.chain.from_iterable(nested))
