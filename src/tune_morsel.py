#! /usr/bin/env python

"""

Example usage:
python src/tune_morsel.py MORSEL/params/dev.txt MORSEL/data/test/brown_wordlist.txt data/morpho-challenge/en/all_analyses morsel_tuning/brown --workers 8 > morsel_tuning/brown/results.tsv
"""

import itertools
import multiprocessing
import os
import subprocess
from argparse import ArgumentParser
from operator import itemgetter
from pathlib import Path
from typing import Dict, Tuple, Any

SEARCH_PARAMS = {
    "transform_length_weighting_exponent": (1.0, 1.25, 1.5, 2.0),
    "precision_threshold": (0.1, 0.075, 0.05, 0.025, 0.01),
}
PARAM_FILENAME = "params.txt"


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("base_param_file", type=Path, help="base param file to modify")
    parser.add_argument("word_list", type=Path, help="word list to train on")
    parser.add_argument(
        "gold_analyses", type=Path, help="gold analyses to use for evaluation"
    )
    parser.add_argument("output_dir", type=Path, help="output_directory")
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="number of parallel workers to use to run MORSEL",
    )
    args = parser.parse_args()
    tune_morsel(
        args.base_param_file,
        args.word_list,
        args.gold_analyses,
        args.output_dir,
        args.workers,
    )


def tune_morsel(
    base_params: Path,
    word_list: Path,
    gold_analyses: Path,
    output_dir: Path,
    workers: int,
) -> None:
    path_configs = gen_params(base_params, output_dir, SEARCH_PARAMS)

    pool = multiprocessing.Pool(workers)
    results = pool.starmap(
        run_config,
        [
            (path, config, word_list, gold_analyses)
            for path, config in path_configs.items()
        ],
    )

    # Sort by best F1
    sorted_results = sorted(results, key=itemgetter(2), reverse=True)

    # Grab field names from a sample configuration
    param_names = [param[0] for param in sorted_results[0][1]]

    # Print results
    header = ["Path"] + param_names + ["F1"]
    print("\t".join(header))
    for path, config, score in sorted_results:
        param_values = [str(item[1]) for item in config]
        row = [str(path)] + param_values + [str(score)]
        print("\t".join(row))


def gen_params(
    base_param_path: Path, output_dir: Path, search_params: Dict[str, Tuple[Any]]
) -> Dict[Path, Tuple[Tuple[str, Any], ...]]:
    path_params = {}
    param_lines = ["# Fixed parameters"]
    with base_param_path.open(encoding="utf8") as param_file:
        for line in param_file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            param_name = line.split("=")[0].strip()
            if param_name not in SEARCH_PARAMS:
                param_lines.append(line)
    param_lines.append("")
    param_lines.append("# Parameters being searched")

    keys = tuple(search_params)
    vals = tuple(search_params.values())
    param_num = 0
    for combination in itertools.product(*vals):
        assert len(keys) == len(combination)
        config = tuple((key, val) for key, val in zip(keys, combination))
        config_dir = output_dir / str(param_num)
        path_params[config_dir] = config

        additional_lines = [
            f"{key_name} = {key_value}"
            for key_name, key_value in zip(keys, combination)
        ]

        os.makedirs(config_dir, exist_ok=True)
        with (config_dir / PARAM_FILENAME).open("w", encoding="utf8") as param_file:
            param_file.write("\n".join(param_lines + additional_lines) + "\n")
        param_num += 1

    return path_params


def run_config(
    path: Path,
    config: Tuple[Tuple[str, Any], ...],
    word_list: Path,
    gold_analyses: Path,
) -> Tuple[Path, Tuple[Tuple[str, Any], ...], float]:
    param_path = path / PARAM_FILENAME
    score = subprocess.check_output(
        [
            "bash",
            "src/morsel-train-eval.sh",
            str(word_list),
            str(param_path),
            str(gold_analyses),
            str(path),
        ]
    )
    score = float(score)
    return path, config, score


if __name__ == "__main__":
    main()
