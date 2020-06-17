# Factorial experiment for evaluating Unimorph vs MC 2010 Dev Set Data
# 2 x 2 conditions
#  - language: {finnish, german}
#  - POS: {with POS, without POS}

echo "\n### Finnish, POS included\n"
./eval_fin_wpos.sh

echo "\n### Finnish, POS excluded\n"
./eval_fin_nopos.sh

echo "\n### German, POS included\n"
./eval_deu_wpos.sh

echo "\n### German, POS excluded\n"
./eval_deu_nopos.sh
