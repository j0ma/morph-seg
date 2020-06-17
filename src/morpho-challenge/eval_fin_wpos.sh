GOLDSTD_PAIRS="../mc_data/fin/dev/goldstd_develset.wordpairs.fin.utf8"
GOLDSTD_FILE="../mc_data/fin/dev/goldstd_develset.labels.fin.utf8"
RESULTS_PAIRS="../unimorph/wordpairs/unimorph.fin.wordpairs"
RESULTS_FILE="../unimorph/filtered/unimorph_fin_filtered_for_mcdev_nolemma"

perl eval_morphemes_v2.pl $GOLDSTD_PAIRS $RESULTS_PAIRS $GOLDSTD_FILE $RESULTS_FILE
