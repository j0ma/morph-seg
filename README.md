# Morphological / BPE segmentation experiments

## Morpho Challenge Eval - 07/01/2020

These models were trained on Flores data, applied to Flores/Brown data, and evaluated with respect to the Morpho Challenge 2010 gold standard analyses.

**NOTE**: The model binaries used can be found in `./bin/cache-070120`. New models will be added, as the performance on Flores data with these parameters is quite abysmal. 

### Flores
```
### flatcat

#
PART0. Precision: 13.61% (20/147); non-affixes: 13.61% (20/147); affixes: 100.00% (0/0)
PART0. Recall:    0.86% (6/759); non-affixes: 1.15% (4/390); affixes: 0.54% (2/369)
PART0. F-measure: 1.61%; non-affixes: 2.13%; affixes: 1.08%
#
TOTAL. Precision: 13.61%; non-affixes: 13.61%; affixes: 100.00%
TOTAL. Recall:    0.86%; non-affixes: 1.15%; affixes: 0.54%
TOTAL. F-measure: 1.61%; non-affixes: 2.13%; affixes: 1.08%

### lmvr

#
PART0. Precision: 11.76% (79/669); non-affixes: 17.69% (47/264); affixes: 7.91% (32/405)
PART0. Recall:    4.34% (33/759); non-affixes: 7.12% (28/390); affixes: 1.41% (5/369)
PART0. F-measure: 6.34%; non-affixes: 10.15%; affixes: 2.39%
#
TOTAL. Precision: 11.76%; non-affixes: 17.69%; affixes: 7.91%
TOTAL. Recall:    4.34%; non-affixes: 7.12%; affixes: 1.41%
TOTAL. F-measure: 6.34%; non-affixes: 10.15%; affixes: 2.39%

### morsel
#
PART0. Precision: 78.74% (450/572); non-affixes: 84.91% (94/110); affixes: 77.27% (357/462)
PART0. Recall:    52.24% (392/751); non-affixes: 34.25% (135/393); affixes: 72.00% (258/358)
PART0. F-measure: 62.81%; non-affixes: 48.81%; affixes: 74.54%
#
TOTAL. Precision: 78.74%; non-affixes: 84.91%; affixes: 77.27%
TOTAL. Recall:    52.24%; non-affixes: 34.25%; affixes: 72.00%
TOTAL. F-measure: 62.81%; non-affixes: 48.81%; affixes: 74.54%

```


### Brown
```
### flatcat

#
PART0. Precision: 69.63% (94/135); non-affixes: 69.63% (94/135); affixes: 100.00% (0/0)
PART0. Recall:    7.30% (29/396); non-affixes: 10.24% (23/223); affixes: 3.51% (6/173)
PART0. F-measure: 13.21%; non-affixes: 17.86%; affixes: 6.77%
#
TOTAL. Precision: 69.63%; non-affixes: 69.63%; affixes: 100.00%
TOTAL. Recall:    7.30%; non-affixes: 10.24%; affixes: 3.51%
TOTAL. F-measure: 13.21%; non-affixes: 17.86%; affixes: 6.77%

### lmvr

#
PART0. Precision: 50.54% (372/736); non-affixes: 34.00% (87/255); affixes: 59.33% (285/481)
PART0. Recall:    30.30% (232/766); non-affixes: 36.32% (147/405); affixes: 23.53% (85/361)
PART0. F-measure: 37.88%; non-affixes: 35.12%; affixes: 33.70%
#
TOTAL. Precision: 50.54%; non-affixes: 34.00%; affixes: 59.33%
TOTAL. Recall:    30.30%; non-affixes: 36.32%; affixes: 23.53%
TOTAL. F-measure: 37.88%; non-affixes: 35.12%; affixes: 33.70%

### morsel

#
PART0. Precision: 71.85% (477/664); non-affixes: 82.69% (92/111); affixes: 69.68% (385/553)
PART0. Recall:    52.35% (401/766); non-affixes: 38.93% (158/405); affixes: 67.42% (243/361)
PART0. F-measure: 60.57%; non-affixes: 52.94%; affixes: 68.53%
#
TOTAL. Precision: 71.85%; non-affixes: 82.69%; affixes: 69.68%
TOTAL. Recall:    52.35%; non-affixes: 38.93%; affixes: 67.42%
TOTAL. F-measure: 60.57%; non-affixes: 52.94%; affixes: 68.53%

```

## Notes
- `src/indic` taken from main [FLoRes repo](https://github.com/j0ma/flores)
- `download-data.sh` is also from flores, with slight path modifications. Same goes for `prepare-*.sh`
    - note: the script downloads excess data
- `src/create-flores-vocabulary.py` uses `sacremoses` for tokenizing English. Segmentations are **NOT** learned from untokenized text like with `SentencePiece` in the original Flores paper.
