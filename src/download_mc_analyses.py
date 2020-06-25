#! /usr/bin/env python
"""Download Morpho Challenge gold standards and combine all data in each language.

Currently only gets English data.
"""

import subprocess
import urllib.request
from pathlib import Path

import click

# We don't use the 2005 data since the gold standard was preprocessed differently
# You can find it at:
# http://morpho.aalto.fi/events/morphochallenge2005/data/goldstdsample.eng
LANGS = ("eng",)
DEV_FILES = {
    "eng": {
        "2010": "http://morpho.aalto.fi/events/morphochallenge2010/data/goldstd_develset.labels.eng",
        "2009": "http://morpho.aalto.fi/events/morphochallenge2009/data/goldstdsample.eng",
        "2008": "http://morpho.aalto.fi/events/morphochallenge2008/data/goldstdsample.eng",
        "2007": "http://morpho.aalto.fi/events/morphochallenge2007/data/goldstdsample.eng",
    }
}
TRAIN_FILES = {
    "eng": {
        "2010": "http://morpho.aalto.fi/events/morphochallenge2010/data/goldstd_trainset.labels.eng",
    }
}


@click.command()
@click.argument("path")
def main(path: str):
    """Download Morpho Challenge english analyses to PATH"""
    output_dir = Path(path)
    output_dir.mkdir(exist_ok=True)

    for lang in LANGS:
        analysis_paths = []
        for datasets, set_name in ((DEV_FILES, "dev"), (TRAIN_FILES, "train")):
            for year, url in datasets[lang].items():
                filename = f"{set_name}_analyses.{year}.{lang}"
                analysis_path = output_dir / filename
                urllib.request.urlretrieve(url, analysis_path)
                analysis_paths.append(str(analysis_path))

        # Concatenate all the files and filter for duplicates
        cmd = f"cat {' '.join(analysis_paths)} | sort | uniq > {output_dir / f'all_analyses.{lang}'}"
        subprocess.check_call(cmd, shell=True)


if __name__ == "__main__":
    main()
