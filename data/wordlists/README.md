Data from flores added here came from MT preprocessing, specifically:
```
lignos05:/home/jonne/flores/data/wiki_ne_en_lmvr/train.en.tok.lower
lignos05:/home/jonne/flores/data/wiki_ne_en_lmvr/train.ne.tok.lower
lignos05:/home/jonne/flores/data/wiki_si_en_lmvr/train.en.tok.lower
lignos05:/home/jonne/flores/data/wiki_si_en_lmvr/train.si.tok.lower
```

Wordlists were then made using `make_mc_wordlist`, for example:
```
python src/make_mc_wordlist.py < data/tokenized/ne_en/train.en.tok.lower > data/tokenized/ne_en/train.en.wordlist
```
