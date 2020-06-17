import helpers as h
import morfessor
import flatcat
import pickle
import click
import os

# SUPPORTED FLATCAT MODEL VARIANTS:
# - 'batch' 

@click.command()
@click.option('--lang', required=True)
@click.option('--input-path', '-i',
              help="Path to input wordlist.",
              type=click.Path(exists=True))
@click.option('--output', '-o',
               help="Folder to save segmentations in.",
               type=click.Path())
@click.option('--model-type', default='batch')
@click.option('--model-output-path', help="Path to save model binary in", default=None)
@click.option('--construction-separator', default=' + ')
def main(lang, input_path, output, model_type, model_output_path, construction_separator):
    # load data
    p, f = os.path.split(input_path)
    file_name, extension = os.path.splitext(f)

    INPUT_PATH = os.path.abspath(input_path)
    OUTPUT_FOLDER = os.path.abspath(output)

    # make output folder if it doesn't exist
    if not os.path.exists(OUTPUT_FOLDER):
        print(f'Not found: {OUTPUT_FOLDER}. Creating...')
        os.system(f'mkdir -p {OUTPUT_FOLDER}')

    if model_type == 'all': 
        models = ['flatcat-batch']
    else:
        models = [f'flatcat-{model_type}']
        
    print('Models to run:\n - {}'.format("\n - ".join(models)))
    for model in models:
        h.train_model(lang=lang,
                model_name=model,
                input_path=INPUT_PATH,
                input_file_name=file_name,
                model_output_path=model_output_path,
                segm_output_folder=OUTPUT_FOLDER)

if __name__ == '__main__':
    main()
