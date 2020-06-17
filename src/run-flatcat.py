import helpers as h
import morfessor
import flatcat
import pickle
import click
import os

@click.command()
@click.option('--input-path', 
              default="../data/raw/brown_wordlist", 
              help="Path to input wordlist. [NB: file, not folder!]",
              type=click.Path(exists=True))
@click.option('--output', '-o', 
               default="../data/segmented/", 
               help="Folder to save segmentations in. [NB: folder, not file!]",
               type=click.Path(exists=True))
@click.option('--model-type', default='all')
@click.option('--construction-separator', default=' + ')
def main(input_path, output, model_type, construction_separator):
    # load data
    p, f = os.path.split(input_path)
    file_name, extension = os.path.splitext(f)

    INPUT_PATH = os.path.abspath(input_path)
    OUTPUT_FOLDER = os.path.abspath(output)

    models = ['flatcat-batch']
    functions = [
            lambda mn, ip: h.run_morfessor_flatcat(mn, ip, construction_separator=construction_separator),
            lambda mn, ip: h.run_morfessor_flatcat(mn, ip, construction_separator=construction_separator)
    ]
    if model_type == 'all': 
        print('Models to run:\n - {}'.format("\n - ".join(models)))
        for model, run in zip(models, functions):
            output_filename = f"{file_name}.segmented.{model}"
            OUTPUT_PATH = os.path.join(OUTPUT_FOLDER, output_filename)
            
            print(f'Now running: {model}')
            model_bin, words, segmentations = run(model, INPUT_PATH)
            if words is not None and segmentations is not None:
                output_lines = [f"{w}\t{s}" for w, s in zip(words, segmentations)]
                h.write_file(output_lines, OUTPUT_PATH)
            else:
                print('No segmentations received, not going to write to disk...')
            
            # save model to pickle
            if model_bin is not None:
                h.dump_pickle(model_bin, f"{OUTPUT_FOLDER}/../../bin/{file_name}-{model}.bin")
            else:
                print('No model received, not going to write to disk...')
    else:
        raise NotImplementedError('Individual models not implemented yet!')

if __name__ == '__main__':
    main()
