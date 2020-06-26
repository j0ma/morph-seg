#! /usr/bin/env python
"""Download Morpho Challenge gold standards and combine all data in each language.

Currently only gets English data.
"""

import subprocess
import urllib.request
from pathlib import Path
from typing import List

import click

# We use en instead of eng to match the translation data
LANGS = ("en",)
# We don't use the 2005 data since the gold standard was preprocessed differently
# You can find it at:
# http://morpho.aalto.fi/events/morphochallenge2005/data/goldstdsample.eng
DEV_FILES = {
    "en": {
        "2010": "http://morpho.aalto.fi/events/morphochallenge2010/data/goldstd_develset.labels.eng",
        "2009": "http://morpho.aalto.fi/events/morphochallenge2009/data/goldstdsample.eng",
        "2008": "http://morpho.aalto.fi/events/morphochallenge2008/data/goldstdsample.eng",
        "2007": "http://morpho.aalto.fi/events/morphochallenge2007/data/goldstdsample.eng",
    }
}
TRAIN_FILES = {
    "en": {
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
        lang_dir = output_dir / lang
        lang_dir.mkdir(exist_ok=True)
        analysis_paths: List[str] = []
        for datasets, set_name in ((DEV_FILES, "dev"), (TRAIN_FILES, "train")):
            for year, url in datasets[lang].items():
                filename = f"{set_name}_analyses.{year}"
                analysis_path = lang_dir / filename
                urllib.request.urlretrieve(url, analysis_path)
                analysis_paths.append(str(analysis_path))

        # Concatenate all the files and filter for duplicates
        all_analyses_path = lang_dir / "all_analyses"
        cmd = f"cat {' '.join(analysis_paths)} | sort | uniq > {all_analyses_path}"
        subprocess.check_call(cmd, shell=True)


if __name__ == "__main__":
    main()
