# Using MORSEL

MORSEL is used as a submodule, so you'll have to initialize and update the module before using it.

All scripts below must be run from the root of the morph-seg repository.

* MORSEL is built by running `src/build-morsel.sh`

## Tuning Experiments

The following process was used for the tuning experiments:

* Download the MC data: `./src/download_mc_analyses.py data/morpho-challenge`
* Create wordlists for each language. Copy a lowercased, Moses-tokenized training data file and turn it into a wordlist, for example: `python src/make_mc_wordlist.py < data/tokenized/ne_en/train.en.tok.lower > data/tokenized/ne_en/train.en.wordlist`. The wordlists used for tuning are checked in at `data/wordlists/`.
* Run tuning: `src/run-morsel-tuning.sh`. This writes output to `/tuning/morsel`. Results have been manually concatenated for analysis in the `all_results.{xlsx,tsv} files in that directory.
* The tuning suggested the following params, which were chosen by highest average F1 across the English side of the flores training data for NE-EN and SI-EN (choosing by best average rank across the two data sets produces the same result):
```
transform_length_weighting_exponent = 1.5
precision_threshold = 0.075
```
* These params were saved in `params/morsel/tuned.txt`


## Applying MORSEL + BPE to the Flores data

Now that the parameters are tuned, we can apply MORSEL and BPE together:

* Run `src/run-morsel-bpe-flores.sh`. It will automatically use the tuned parameters and the wordlists from the training data, and writes output to `data/segmented/flores/morsel/`. Note that the number of units in the output isn't exact. You can check as follows:
```
grep "MORSEL + BPE segmentation vocab size" data/segmented/flores/morsel/*/*/run.log
data/segmented/flores/morsel/ne_en/en/run.log:MORSEL + BPE segmentation vocab size: 2393
data/segmented/flores/morsel/ne_en/ne/run.log:MORSEL + BPE segmentation vocab size: 2378
data/segmented/flores/morsel/si_en/en/run.log:MORSEL + BPE segmentation vocab size: 2510
data/segmented/flores/morsel/si_en/si/run.log:MORSEL + BPE segmentation vocab size: 2444
```
* To use the segmentation from MORSEL, get the correct word -> MORSEL + BPE map for the language you're using. For example, `data/segmented/flores/morsel/ne_en/en/morsel_seg_bpe_map.txt`.
* You'll use this map to transform an in-vocabulary words, which should cover all of training, but not all of dev and test.
* To cover the remaining words in dev and test, you'll want to make a list of the words in dev and test that this doesn't cover, and use `subword-nmt apply-bpe` using the BPE code that MORSEL used on the stems, for example (`data/segmented/flores/morsel/ne_en/en/stem_code.txt`)
* The MORSEL + BPE script also creates BPE codes and output for applying BPE directly to words (no MORSEL). These files are prefixed with `word` (e.g. `word_code.txt`, `words_bpe_map.txt`). Do not use these except for the purpose of comparing pure BPE vs. MORSEL + BPE.


## Applying MORSEL + BPE to the Flores data

Run `./src/run-morsel-bpe-wmt19.sh`. It will automatically print the resulting vocab sizes:
```
data/segmented/wmt19/morsel/gu_en/en/run.log:MORSEL + BPE segmentation vocab size: 2474
data/segmented/wmt19/morsel/gu_en/gu/run.log:MORSEL + BPE segmentation vocab size: 2415
data/segmented/wmt19/morsel/kk_en/en/run.log:MORSEL + BPE segmentation vocab size: 2458
data/segmented/wmt19/morsel/kk_en/kk/run.log:MORSEL + BPE segmentation vocab size: 2423
```
