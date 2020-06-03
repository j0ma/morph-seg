from collections import Counter
import helpers as h
import morfessor
import flatcat
import pickle
import click
import os

@click.command()
@click.option('--input-path', 
              default="../data/raw/brown_wordlist", 
              type=click.Path(exists=True))
@click.option('--output-folder', 
               default="../data/segmented/", 
               type=click.Path(exists=True))
@click.option('--model-type', default='baseline')
def main(input_path, output_folder, model_type):
    # load data
    p, f = os.path.split(input_path)
    file_name, extension = os.path.splitext(f)

    INPUT_PATH = os.path.abspath(input_path)
    OUTPUT_FOLDER = os.path.abspath(output_folder)

    models = [f"morfessor-baseline-{tr}" for tr in 
              ('batch-recursive', 'batch-viterbi', 
               'online-recursive', 'online-viterbi')]
    functions = [
            lambda mn, ip: h.run_morfessor_baseline(mn, ip),
            lambda mn, ip: h.run_morfessor_baseline(mn, ip),
            lambda mn, ip: h.run_morfessor_baseline(mn, ip),
            lambda mn, ip: h.run_morfessor_baseline(mn, ip),
    ]
    if model_type == 'all': 
        print('Models to run:\n - {}'.format("\n - ".join(models)))
        for model, run in zip(models, functions):
            output_filename = f"{file_name}.segmented.{model}"
            segmentation_filename = f"{output_filename}.segmentation-only"
            OUTPUT_PATH = os.path.join(OUTPUT_FOLDER, output_filename)
            SEGM_PATH = os.path.join(OUTPUT_FOLDER, segmentation_filename)

            print(f'Now running: {model}')
            model_bin, words, segmentations = run(model, INPUT_PATH)
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
                h.dump_pickle(model_bin, f"{OUTPUT_FOLDER}/../../bin/{model}.bin")
            else:
                print('No model received, not going to write to disk...')
    elif model_type == 'baseline':

        # oof this feels so un-pythonic
        model = "morfessor-baseline-batch-recursive"
        run = lambda mn, ip: h.run_morfessor_baseline(mn, ip)
        
        print('Running baseline model only...')
        output_filename = f"{file_name}.segmented.{model}"
        segmentation_filename = f"{output_filename}.segmentation-only"
        OUTPUT_PATH = os.path.join(OUTPUT_FOLDER, output_filename)
        SEGM_PATH = os.path.join(OUTPUT_FOLDER, segmentation_filename)
        
        print(f'Now running: {model}')
        model_bin, words, segmentations = run(model, INPUT_PATH)
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
            h.dump_pickle(model_bin, f"{OUTPUT_FOLDER}/../../bin/{model}.bin")
        else:
            print('No model received, not going to write to disk...')

if __name__ == '__main__':
    main()






