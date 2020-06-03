import morfessor
import flatcat
import pickle
import click
import os

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

    segmentations = [model.viterbi_segment(w) for w in train_words]

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
    segmentations = [" ".join(model.viterbi_segment(w)[0]) for w in train_words]

    return model, train_words, segmentations

def dump_pickle(obj, f):
    with open(f, 'wb') as f:
        pickle.dump(obj, f)

def write_file(lines, f):
    with open(f, 'w') as f:
        f.write("\n".join(lines))
