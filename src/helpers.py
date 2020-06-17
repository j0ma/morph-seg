from collections import Counter
import sacremoses as sm
import itertools as it
import morfessor
import flatcat
import pickle
import click
import os

def train_model(lang, 
        model_name, 
        input_path, 
        input_file_name, 
        model_output_path, 
        segm_output_folder, 
        corpus_weight=1.0,
        construction_separator=" + "):
    """
    Description
    ------------
    Trains the Morfessor Baseline model. 
    After training, dumps model binary to disk 
    and performs segmentation on the training data.

    Parameters
    ----------
    lang: str
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
    if 'flatcat' in model:
        run = lambda mn, ip: run_morfessor_flatcat(mn, ip, construction_separator=construction_separator, lang=lang)
    else:
        run = run_morfessor_baseline

    model_bin, words, segmentations = run(model , input_path)
    
    segmentation_counts = Counter(segmentations)
    if words is not None and segmentations is not None:
        output_lines = [f"{w}\t{s}" for w, s in zip(words, segmentations)]
        segmentation_lines = [f'{segmentation_counts[s]} {s}' for s in segmentations]
        write_file(output_lines, OUTPUT_PATH)
        write_file(segmentation_lines, SEGM_PATH)
    else:
        print('No segmentations received, not going to write to disk...')
    
    # save model to pickle
    if model_bin is not None:
        bin_path = model_output_path or f"../bin/{input_file_name}-{model}-{lang}.bin"
        dump_pickle(model_bin, bin_path)
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
    return  " ".join(segmentations)

def run_morfessor_flatcat(model_name, input_path, lang='en', seed_segmentation_path=None, construction_separator=" + ", corpus_weight=1.0):

    if seed_segmentation_path is None:
        _ = f"all-flores-words-{lang}.segmented.morfessor-baseline-batch-recursive.segmentation-only"
        seed_segmentation_path = os.path.abspath(f'../data/segmented/flores/{lang}/{_}')

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

    training_type = 'online' if 'online' in model_name else 'batch'
    print('training type = {}'.format(training_type))
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
    with open(f, 'wb') as fout:
        pickle.dump(obj, fout)

def write_file(lines, f):
    with open(f, 'w') as fout:
        fout.write("\n".join(lines))

def read_lines(f):
    with open(f, 'r') as f:
        return [l.strip() for l in f.readlines() if l.strip() != '']

def flatten(nested):
    return list(it.chain.from_iterable(nested))
    
