# Morphological / BPE segmentation experiments

## Notes
- `src/indic` taken from main [FLoRes repo](https://github.com/j0ma/flores)
- `download-data.sh` is also from flores, with slight path modifications. Same goes for `prepare-*.sh`
    - note: the script downloads excess data
- `src/create-flores-vocabulary.py` uses `sacremoses` for tokenizing English. Segmentations are **NOT** learned from untokenized text like with `SentencePiece` in the original Flores paper.
