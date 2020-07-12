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

# Note: 7/11/2020

For some reason LMVR does not like `/` or `\` in the data. Thus, wordlists without those two characters were used.

The files ./*/train.{en,ne,si}.wordlist.noslash were created using:

For example, for SI-EN:

```
grep -v "[0-9]\s[\/\\]$" \
    ./data/wordlists/si_en/train.en.wordlist \
    > ./data/wordlists/si_en/train.en.wordlist.noslash
```

As we can see this reduces the word list by exactly two symbols:

```
% wc -l ./*/train.*.wordlist* 
   62727 ./ne_en/train.en.wordlist
   62725 ./ne_en/train.en.wordlist.noslash
  135663 ./ne_en/train.ne.wordlist
  135661 ./ne_en/train.ne.wordlist.noslash
   69650 ./si_en/train.en.wordlist
   69648 ./si_en/train.en.wordlist.noslash
  174997 ./si_en/train.si.wordlist
  174995 ./si_en/train.si.wordlist.noslash
  886066 total
```
