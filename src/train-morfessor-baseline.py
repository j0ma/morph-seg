import os

import click

import helpers as h

# SUPPORTED BASELINE MODEL VARIANTS:
# - 'batch-recursive'
# - 'batch-viterbi'
# - 'online-recursive'
# - 'online-viterbi'


@click.command()
@click.option("--lang", required=True)
@click.option(
    "--input-path",
    "-i",
    help="Path to input wordlist.",
    type=click.Path(exists=True),
)
@click.option(
    "--output",
    "-o",
    help="Folder to save segmentations in.",
    type=click.Path(),
)
@click.option("--model-type", default="baseline-batch-recursive")
@click.option(
    "--model-output-path", help="Path to save model binary in", default=None
)
def main(lang, input_path, output, model_type, model_output_path):

    # load data
    p, f = os.path.split(input_path)
    file_name, extension = os.path.splitext(f)

    abs_input_path = os.path.abspath(input_path)
    abs_output_folder = os.path.abspath(output)

    # make output folder if it doesn't exist

    if not os.path.exists(abs_output_folder):
        print(f"Not found: {abs_output_folder}. Creating...")
        os.system(f"mkdir -p {abs_output_folder}")

    MODEL_TYPES = {
        "batch-recursive",
        "batch-viterbi",
        "online-recursive",
        "online-viterbi",
    }

    if model_type not in MODEL_TYPES:
        raise ValueError(f"Model type must be one of {MODEL_TYPES}")

    if model_type == "all":
        models = [f"baseline-{tr}" for tr in MODEL_TYPES]
    else:
        models = [f"baseline-{model_type}"]

    print("Models to run:\n - {}".format("\n - ".join(models)))

    for model in models:
        h.train_model(
            lang=lang,
            model_name=model,
            input_path=abs_input_path,
            input_file_name=file_name,
            model_output_path=model_output_path,
            segm_output_folder=abs_output_folder,
        )


if __name__ == "__main__":
    main()
