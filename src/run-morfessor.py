import morfessor
import flatcat
import pickle
import click
import os

def dump_pickle(obj, f):
    with open(f, 'wb') as f:
        pickle.dump(obj, f)

def write_file(lines, f):
    with open(f, 'w') as f:
        f.write("\n".join(lines))

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

def run_morfessor_flatcat(model_name, input_path, seed_segmentation_path):

    if seed_segmentation_path is None:
        _ = "brown_wordlist.segmented.morfessor-baseline-batch-recursive.txt"
        seed_segmentation_path = os.path.abspath(f'../data/segmented/{_}')

    io = flatcat.FlatcatIO(construction_separator="\t")

    train_data = [t for t in io.read_corpus_list_file(input_path)]
    train_words = [w for _, w, _ in train_data]

    morph_usage = flatcat.categorizationscheme.MorphUsageProperties()
    model = flatcat.FlatcatModel(morph_usage, corpusweight=1.0)

    # this might result in overfit, change later(?)
    model.add_corpus_data(io.read_segmentation_file(seed_segmentation_path))
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

@click.command()
@click.option('--input-path', 
              default="../data/raw/brown_wordlist.txt", 
              type=click.Path(exists=True))
@click.option('--output-folder', 
               default="../data/segmented/", 
               type=click.Path(exists=True))
<<<<<<< HEAD
@click.option('--model-type', default='baseline')
def main(input_path, output_folder, model_type):
=======
def main(input_path, output_folder):
>>>>>>> 856af8cfbaad157e5fadf38111ea1048f98eb3bb
    # load data
    p, f = os.path.split(input_path)
    file_name, extension = os.path.splitext(f)

    INPUT_PATH = os.path.abspath(input_path)
    OUTPUT_FOLDER = os.path.abspath(output_folder)

    models = [f"morfessor-baseline-{tr}" for tr in 
              ('batch-recursive', 'batch-viterbi', 
               'online-recursive', 'online-viterbi')]
    models = models + ['flatcat-batch', 'flatcat-online']
    functions = [
            lambda mn, ip: run_morfessor_baseline(mn, ip),
            lambda mn, ip: run_morfessor_baseline(mn, ip),
            lambda mn, ip: run_morfessor_baseline(mn, ip),
            lambda mn, ip: run_morfessor_baseline(mn, ip),
            lambda mn, ip: run_morfessor_flatcat(mn, ip, None),
            lambda mn, ip: run_morfessor_flatcat(mn, ip, None)
    ]
<<<<<<< HEAD
    if model_type == 'all': 
        print('Models to run:\n - {}'.format("\n - ".join(models)))
        for model, run in zip(models, functions):
            output_filename = f"{file_name}.segmented.{model}{extension}"
            OUTPUT_PATH = os.path.join(OUTPUT_FOLDER, output_filename)
            
            print(f'Now running: {model}')
            model_bin, words, segmentations = run(model, INPUT_PATH)
            if words is not None and segmentations is not None:
                output_lines = [f"{w}\t{s}" for w, s in zip(words, segmentations)]
                write_file(output_lines, OUTPUT_PATH)
            else:
                print('No segmentations received, not going to write to disk...')
            
            # save model to pickle
            if model_bin is not None:
                dump_pickle(model_bin, f"{OUTPUT_FOLDER}/../../bin/{model}.bin")
            else:
                print('No model received, not going to write to disk...')
    elif model_type == 'baseline':

        # oof this feels so un-pythonic
        model = "morfessor-baseline-batch-recursive"
        run = lambda mn, ip: run_morfessor_baseline(mn, ip)
        
        print('Running baseline model only...')
=======
    
    print('Models to run:\n - {}'.format("\n - ".join(models)))
    for model, run in zip(models, functions):
>>>>>>> 856af8cfbaad157e5fadf38111ea1048f98eb3bb
        output_filename = f"{file_name}.segmented.{model}{extension}"
        OUTPUT_PATH = os.path.join(OUTPUT_FOLDER, output_filename)
        
        print(f'Now running: {model}')
        model_bin, words, segmentations = run(model, INPUT_PATH)
        if words is not None and segmentations is not None:
            output_lines = [f"{w}\t{s}" for w, s in zip(words, segmentations)]
            write_file(output_lines, OUTPUT_PATH)
        else:
            print('No segmentations received, not going to write to disk...')
        
        # save model to pickle
        if model_bin is not None:
            dump_pickle(model_bin, f"{OUTPUT_FOLDER}/../../bin/{model}.bin")
        else:
            print('No model received, not going to write to disk...')

<<<<<<< HEAD


=======
>>>>>>> 856af8cfbaad157e5fadf38111ea1048f98eb3bb
if __name__ == '__main__':
    main()






