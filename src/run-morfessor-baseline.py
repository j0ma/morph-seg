from collections import Counter
import helpers as h
import morfessor
import pickle
import click
import os

# SUPPORTED BASELINE MODEL VARIANTS:
# - 'batch-recursive' 
# - 'batch-viterbi' 
# - 'online-recursive' 
# - 'online-viterbi'

@click.command()
@click.option('--lang', required=True)
@click.option('--input-path', '-i',
              default="../data/raw/brown_wordlist", 
              help="Path to input wordlist.",
              type=click.Path(exists=True))
@click.option('--output', '-o',
               default="../data/segmented/", 
               help="Folder to save segmentations in.",
               type=click.Path(exists=True))
@click.option('--model-type', default='baseline-batch-recursive')
@click.option('--model-output-path', help="Path to save model binary in", default=None)
def main(lang, input_path, output, model_type, model_output_path):

    # load data
    p, f = os.path.split(input_path)
    file_name, extension = os.path.splitext(f)

    INPUT_PATH = os.path.abspath(input_path)
    OUTPUT_FOLDER = os.path.abspath(output)
    MODEL_TYPES = {'batch-recursive', 'batch-viterbi', 
                   'online-recursive', 'online-viterbi'}

    if model_type not in MODEL_TYPES:
        raise ValueError(f"Model type must be one of {MODEL_TYPES}")

    if model_type == 'all': 
        models = [f"baseline-{tr}" for tr in MODEL_TYPES]
    else:
        models = [f'baseline-{model_type}']
        
    print('Models to run:\n - {}'.format("\n - ".join(models)))
    for model in models:
        h.train_model(lang=lang,
                model_name=model,
                input_path=INPUT_PATH,
                input_file_name=file_name,
                model_output_path=model_output_path,
                segm_output_path)


if __name__ == '__main__':
    main()






