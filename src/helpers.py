import sacremoses as sm
import itertools as it
import morfessor
import flatcat
import pickle
import click
import os

def train_model(model_name, 
        input_path, 
        input_file_name, 
        model_output_path, 
        segm_output_folder):
    """
    Description
    ------------
    Trains the Morfessor Baseline model. 
    After training, dumps model binary to disk 
    and performs segmentation on the training data.

    Parameters
    ----------
    model_name: str
    input_path: str
        Path to input wordlist
    input_file_name: str
    model_output_path: str
    segm_output_folder: str
        Path to segmentation output folder
    """
    model = f"morfessor-{model_name}"
    output_filename = f"{input_file_name}.segmented.{model}"
    segmentation_filename = f"{output_filename}.segmentation-only"
    OUTPUT_PATH = os.path.join(segm_output_folder, output_filename)
    SEGM_PATH = os.path.join(segm_output_folder, segmentation_filename)
    
    print(f'Now running: {model}')
    model_bin, words, segmentations = \
            h.run_morfessor_baseline(model, input_path)
    
    segmentation_counts = Counter(segmentations)
    if words is not None and segmentations is not None:
        output_lines = [f"{w}\t{s}" for w, s in zip(words, segmentations)]
        segmentation_lines = [f'{segmentation_counts[s]} {s}' for s in segmentations]
        h.write_file(output_lines, OUTPUT_PATH)
        h.write_file(segmentation_lines, SEGM_PATH)
    else:
        print('No segmentations received, not going to write to disk...')
    
    # save model to pickle
    if model_bin is not None:
        bin_path = model_output_path or f"{OUTPUT_FOLDER}/../../bin/{input_file_name}-{model}.bin")
        h.dump_pickle(model_bin, bin_path)
    else:
        print('No model received, not going to write to disk...')

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
        out = model.viterbi_segment(w)
    return out

def segment_sentence(model, sentence, tokenizer=None):
    """
    Description
    -----------
    Segments `sentence` using `model` and `tokenizer`.

    Parameters
    ----------
    model: Morfessor model
        - in reality this can be anything that supports
          the .segment() method
    """
    if tokenizer is None:
        tokenizer = sm.MosesTokenizer('en')
    words = tokenizer.tokenzie(sentence)
    segmentations = flatten([segment_word(model, w) for w in words])
    return  " ".join(segmentations)

def run_morfessor_flatcat(model_name, input_path, seed_segmentation_path=None, construction_separator=" + ", corpus_weight=1.0):

    if seed_segmentation_path is None:
        _ = "brown_wordlist.segmented.morfessor-baseline-batch-recursive.segmentation-only"
        seed_segmentation_path = os.path.abspath(f'../data/segmented/{_}')

    io = flatcat.FlatcatIO(construction_separator=construction_separator)

    train_data = [t for t in io.read_corpus_list_file(input_path)]
    train_words = [w for _, w, _ in train_data]

    morph_usage = flatcat.categorizationscheme.MorphUsageProperties()
    model = flatcat.FlatcatModel(morph_usage, corpusweight=corpus_weight)
    
    seed_segmentation_file = [
            x for x in io.read_segmentation_file(seed_segmentation_path)
    ]

    print('adding seed segmentations')
    model.add_corpus_data(seed_segmentation_file)
    model.initialize_hmm()

    training_type = model_name.replace('flatcat-','')
    if training_type == 'batch':
        model.train_batch()
    elif training_type == 'online':
        model.train_online(data=(d for d in train_data))
    else:
        raise ValueError("Invalid training method!")

    segmentations = [model.viterbi_segment(w)[0][0] for w in train_words]

    return model, train_words, segmentations

def run_morfessor_baseline(model_name, input_path, hyperparams=None):
    if hyperparams is None:
        hyperparams = {}

    io = morfessor.MorfessorIO()
    train_data = [t for t in io.read_corpus_list_file(input_path)]
   
    training_type = model_name.replace('morfessor-baseline-','')

    model = morfessor.BaselineModel()

    if training_type == 'batch-recursive':
        model.load_data(train_data)
        model.train_batch()
    elif training_type == 'batch-viterbi':
        model.load_data(train_data)
        model.train_batch(algorithm='viterbi')
    elif training_type == 'online-recursive':
        model.train_online(data=(d for d in train_data))
    elif training_type == 'online-viterbi':
        model.train_online(data=(d for d in train_data), algorithm='viterbi')
    else:
        raise ValueError("Invalid training method!")

    train_words = [w for _, w in train_data]
    segmentations = [" ".join(model.segment(w)) for w in train_words]

    return model, train_words, segmentations

def dump_pickle(obj, f):
    with open(f, 'wb') as f:
        pickle.dump(obj, f)

def write_file(lines, f):
    with open(f, 'w') as f:
        f.write("\n".join(lines))

def read_lines(f):
    with open(f, 'r') as f:
        return [l.strip() for l in f.readlines() if l.strip() != '']

def flatten(nested):
    return list(it.chain.from_iterable(nested))
