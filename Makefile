all: init install_lmvr download prep flores

flores: create_flores_vocab train_morfessor train_lmvr

install_lmvr:
	bash ./src/download-lmvr.sh

train_lmvr_tuned_small: train_lmvr_tuned_small_ne train_lmvr_tuned_small_si train_lmvr_tuned_small_en

train_lmvr_tuned_small_ne:
	shuf ./data/raw/flores/wiki_ne_en/flores.vocab.ne.lowercase.withcounts | head -n 20 \
		> ./data/raw/flores/wiki_ne_en/flores.vocab.ne.lowercase.withcounts.small
	bash ./src/train-lmvr-tuned.sh \
		--lang ne \
		--lexicon-size 25 \
		--corpus-name flores.vocab.small \
		--input-path ./data/raw/flores/wiki_ne_en/flores.vocab.ne.lowercase.withcounts.small \
		--segmentation-output-path ./data/segmented/flores/ne \
		--model-output-path ./bin \
		--lexicon-output-path ./data \
		--max-epochs 5

train_lmvr_tuned_small_si:
	shuf ./data/raw/flores/wiki_si_en/flores.vocab.si.lowercase.withcounts | head -n 20 \
		> ./data/raw/flores/wiki_si_en/flores.vocab.si.lowercase.withcounts.small
	bash ./src/train-lmvr-tuned.sh \
		--lang si \
		--lexicon-size 25 \
		--corpus-name flores.vocab.small \
		--input-path ./data/raw/flores/wiki_si_en/flores.vocab.si.lowercase.withcounts.small \
		--segmentation-output-path ./data/segmented/flores/si \
		--model-output-path ./bin \
		--lexicon-output-path ./data \
		--max-epochs 5

train_lmvr_tuned_small_en:
	shuf ./data/raw/flores/flores.vocab.en.lowercase.withcounts | head -n 20 \
		> ./data/raw/flores/flores.vocab.en.lowercase.withcounts.small
	bash ./src/train-lmvr-tuned.sh \
		--lang en \
		--lexicon-size 25 \
		--corpus-name flores.vocab.small \
		--input-path ./data/raw/flores/flores.vocab.en.lowercase.withcounts.small \
		--segmentation-output-path ./data/segmented/flores/en \
		--model-output-path ./bin \
		--lexicon-output-path ./data \
		--max-epochs 5

train_lmvr_tuned_small_si_en:
	shuf ./data/wordlists/si_en/train.en.wordlist | head -20 \
		> /tmp/train.en.wordlist.small
	bash ./src/train-lmvr-tuned.sh \
		--lang si_en \
		--lexicon-size 25 \
		--corpus-name flores.vocab.small \
		--input-path /tmp/train.en.wordlist.small \
		--segmentation-output-path /tmp/ \
		--model-output-path /tmp \
		--lexicon-output-path /tmp/ \
		--max-epochs 5
train_lmvr_tuned: train_lmvr_tuned_ne train_lmvr_tuned_si train_lmvr_tuned_en

# math domain error
train_lmvr_tuned_si_en:
	bash ./src/train-lmvr-tuned.sh \
		--lang si_en \
		--lexicon-size 2500 \
		--corpus-name flores.vocab \
		--input-path ./data/wordlists/si_en/train.en.wordlist.noslash  \
		--segmentation-output-path ./data/segmented/flores/si \
		--model-output-path ./bin \
		--lexicon-output-path ./data \
		--max-epochs 5

# works
train_lmvr_tuned_ne_en:
	bash ./src/train-lmvr-tuned.sh \
		--lang ne_en \
		--lexicon-size 2500 \
		--corpus-name flores.vocab \
		--input-path ./data/wordlists/ne_en/train.en.wordlist.noslash  \
		--segmentation-output-path ./data/segmented/flores/ne \
		--model-output-path ./bin \
		--lexicon-output-path ./data \
		--max-epochs 5

# works
train_lmvr_tuned_ne:
	bash ./src/train-lmvr-tuned.sh \
		--lang ne \
		--lexicon-size 2500 \
		--corpus-name flores.vocab \
		--input-path ./data/wordlists/ne_en/train.ne.wordlist.noslash \
		--segmentation-output-path ./data/segmented/flores/ne \
		--model-output-path ./bin \
		--lexicon-output-path ./data \
		--max-epochs 5

train_lmvr_tuned_si:
	bash ./src/train-lmvr-tuned.sh \
		--lang si \
		--lexicon-size 2500 \
		--corpus-name flores.vocab \
		--input-path ./data/wordlists/si_en/train.si.wordlist.noslash \
		--segmentation-output-path ./data/segmented/flores/si \
		--model-output-path ./bin \
		--lexicon-output-path ./data \
		--max-epochs 5

#train_lmvr_tuned_en:
	#bash ./src/train-lmvr-tuned.sh \
		#--lang en \
		#--lexicon-size 2500 \
		#--corpus-name flores.vocab \
		#--input-path ./data/raw/flores/flores.vocab.en.lowercase.withcounts \
		#--segmentation-output-path ./data/segmented/flores/en \
		#--model-output-path ./bin \
		#--lexicon-output-path ./data \
		#--max-epochs 5

train_lmvr_small: train_lmvr_small_ne train_lmvr_small_si train_lmvr_small_en

train_lmvr_small_ne:
	shuf ./data/raw/flores/wiki_ne_en/flores.vocab.ne.lowercase.withcounts | head -n 20 \
		> ./data/raw/flores/wiki_ne_en/flores.vocab.ne.lowercase.withcounts.small
	bash ./src/train-lmvr.sh \
		--lang ne \
		--lexicon-size 15 \
		--corpus-name flores.vocab.small \
		--input-path ./data/raw/flores/wiki_ne_en/flores.vocab.ne.lowercase.withcounts.small \
		--segmentation-output-path ./data/segmented/flores/ne \
		--model-output-path ./bin \
		--lexicon-output-path ./data \
		--max-epochs 5

train_lmvr_small_si:
	shuf ./data/raw/flores/wiki_si_en/flores.vocab.si.lowercase.withcounts | head -n 20 \
		> ./data/raw/flores/wiki_si_en/flores.vocab.si.lowercase.withcounts.small
	bash ./src/train-lmvr.sh \
		--lang si \
		--lexicon-size 15 \
		--corpus-name flores.vocab.small \
		--input-path ./data/raw/flores/wiki_si_en/flores.vocab.si.lowercase.withcounts.small \
		--segmentation-output-path ./data/segmented/flores/si \
		--model-output-path ./bin \
		--lexicon-output-path ./data \
		--max-epochs 5

train_lmvr_small_en:
	shuf ./data/raw/flores/flores.vocab.en.lowercase.withcounts | head -n 20 \
		> ./data/raw/flores/flores.vocab.en.lowercase.withcounts.small
	bash ./src/train-lmvr.sh \
		--lang en \
		--lexicon-size 15 \
		--corpus-name flores.vocab.small \
		--input-path ./data/raw/flores/flores.vocab.en.lowercase.withcounts.small \
		--segmentation-output-path ./data/segmented/flores/en \
		--model-output-path ./bin \
		--lexicon-output-path ./data \
		--max-epochs 5

train_lmvr: train_lmvr_ne train_lmvr_si train_lmvr_en

train_lmvr_ne:
	bash ./src/train-lmvr.sh \
		--lang ne \
		--lexicon-size 2500 \
		--corpus-name flores.vocab \
	--input-path ./data/raw/flores/wiki_ne_en/flores.vocab.ne.lowercase.withcounts \
	--segmentation-output-path ./data/segmented/flores/ne \
	--model-output-path ./bin \
	--lexicon-output-path ./data \
	--max-epochs 5

train_lmvr_si:
	bash ./src/train-lmvr.sh \
		--lang si \
		--lexicon-size 2500 \
		--corpus-name flores.vocab \
		--input-path ./data/raw/flores/wiki_si_en/flores.vocab.si.lowercase.withcounts \
		--segmentation-output-path ./data/segmented/flores/si \
		--model-output-path ./bin \
		--lexicon-output-path ./data \
		--max-epochs 5

train_lmvr_en:
	bash ./src/train-lmvr.sh \
		--lang en \
		--lexicon-size 2500 \
		--corpus-name flores.vocab \
		--input-path ./data/raw/flores/flores.vocab.en.lowercase.withcounts \
		--segmentation-output-path ./data/segmented/flores/en \
		--model-output-path ./bin \
		--lexicon-output-path ./data \
		--max-epochs 5

train_morfessor: train_morfessor_baseline

#train_flatcat_sh: \
#train_flatcat_sh_ne \
#train_flatcat_sh_en \
#train_flatcat_sh_si

#train_flatcat_sh_en:
#echo "Training Morfessor Flatcat for EN"
#bash ./src/train-flatcat.sh \
	#--lang en \
	#--model-type batch \
	#--model-output-path ./bin \
	#--construction-separator "<ConstSep>" \
	#--perplexity-threshold 10 \
	#--lowercase

#train_flatcat_sh_ne:
#echo "Training Morfessor Flatcat for NE"
#bash ./src/train-flatcat.sh \
	#--lang ne \
	#--model-type batch \
	#--model-output-path ./bin \
	#--construction-separator "<ConstSep>" \
	#--perplexity-threshold 10 \
	#--lowercase

#train_flatcat_sh_si:
#echo "Training Morfessor Flatcat for SI"
#bash ./src/train-flatcat.sh \
	#--lang si \
	#--model-type batch \
	#--model-output-path ./bin \
	#--construction-separator "<ConstSep>" \
	#--perplexity-threshold 10 \
	#--lowercase

#train_flatcat: \
#train_flatcat_ne \
#train_flatcat_si \
#train_flatcat_en

#train_flatcat_en:
#echo "Training Morfessor Flatcat for EN"
#python ./src/train-flatcat.py \
	#--lang en \
	#-i ./data/raw/flores/flores.vocab.en.lowercase.withcounts \
	#-o ./data/segmented/flores/en \
	#--seed-segmentation-path ./data/segmented/flores/en/flores.vocab.en.lowercase.segmented.morfessor-baseline-batch-recursive \
	#--construction-separator "<ConstSep>" \
	#--model-type batch \
	#--model-output-folder ./bin \
	#--lowercase

#train_flatcat_ne:
#echo "Training Morfessor Flatcat for NE"
#python ./src/train-flatcat.py \
	#--lang ne \
	#-i ./data/raw/flores/wiki_ne_en/flores.vocab.ne.lowercase.withcounts \
	#-o ./data/segmented/flores/ne \
	#--seed-segmentation-path ./data/segmented/flores/ne/flores.vocab.ne.lowercase.segmented.morfessor-baseline-batch-recursive \
	#--construction-separator "<ConstSep>" \
	#--model-type batch \
	#--model-output-folder ./bin \
	#--lowercase

#train_flatcat_si:
#echo "Training Morfessor Flatcat for SI"
#python ./src/train-flatcat.py \
	#--lang si \
	#-i ./data/raw/flores/wiki_si_en/flores.vocab.si.lowercase.withcounts \
	#-o ./data/segmented/flores/si \
	#--seed-segmentation-path ./data/segmented/flores/si/flores.vocab.si.lowercase.segmented.morfessor-baseline-batch-recursive \
	#--construction-separator "<ConstSep>" \
	#--model-type batch \
	#--model-output-folder ./bin \
	#--lowercase

train_morfessor_baseline: \
	train_morfessor_baseline_en \
	train_morfessor_baseline_ne \
	train_morfessor_baseline_si

train_morfessor_baseline_en:
	echo "Training Morfessor Baseline for EN"
	python ./src/train-morfessor-baseline.py \
		--lang en \
		-i ./data/raw/flores/flores.vocab.en.lowercase.withcounts \
		-o ./data/segmented/flores/en \
		--construction-separator "<ConstSep>" \
		--model-type batch-recursive \
		--model-output-folder ./bin \
		--corpus-weight 15 \
		--lowercase

train_morfessor_baseline_ne:
	echo "Training Morfessor Baseline for NE"
	python ./src/train-morfessor-baseline.py \
		--lang ne \
		-i ./data/raw/flores/wiki_ne_en/flores.vocab.ne.lowercase.withcounts \
		-o ./data/segmented/flores/ne \
		--construction-separator "<ConstSep>" \
		--model-type batch-recursive \
		--model-output-folder ./bin \
		--corpus-weight 15 \
		--lowercase

train_morfessor_baseline_si:
	echo "Training Morfessor Baseline for SI"
	python ./src/train-morfessor-baseline.py \
		--lang si \
		-i ./data/raw/flores/wiki_si_en/flores.vocab.si.lowercase.withcounts \
		-o ./data/segmented/flores/si \
			--construction-separator "<ConstSep>" \
			--model-type batch-recursive \
			--model-output-folder ./bin \
			--corpus-weight 15 \
			--lowercase

create_flores_vocab: \
	create_flores_vocab_en \
	create_flores_vocab_ne \
	create_flores_vocab_si
	bash ./src/remove-slash-from-wordlists.sh

create_flores_vocab_en:
	echo "Creating vocabulary for EN"
	bash ./src/create-flores-vocabulary.sh \
		--lang en \
		--raw-data-folder data/raw \
		--output-file data/raw/flores/flores.vocab.en.lowercase.withcounts \
		--with-counts

	cut \
		-d' ' -f 2- \
		data/raw/flores/flores.vocab.en.lowercase.withcounts \
		> data/raw/flores/flores.vocab.en.lowercase

create_flores_vocab_ne:
	echo "Creating vocabulary for NE"
	bash ./src/create-flores-vocabulary.sh \
		--lang ne \
		--raw-data-folder data/raw \
		--output-file data/raw/flores/wiki_ne_en/flores.vocab.ne.lowercase.withcounts \
		--with-counts

	cut \
		-d' ' -f 2- \
		data/raw/flores/wiki_ne_en/flores.vocab.ne.lowercase.withcounts \
		> data/raw/flores/wiki_ne_en/flores.vocab.ne.lowercase

create_flores_vocab_si:
	echo "Creating vocabulary for SI"
	bash ./src/create-flores-vocabulary.sh \
		--lang si \
		--raw-data-folder data/raw \
		--output-file data/raw/flores/wiki_si_en/flores.vocab.si.lowercase.withcounts \
		--with-counts

	cut \
		-d' ' -f 2- \
		data/raw/flores/wiki_si_en/flores.vocab.si.lowercase.withcounts \
		> data/raw/flores/wiki_si_en/flores.vocab.si.lowercase


package_segmentation_models:
	mkdir -p segmentation-models
	cp ./bin/*.{bin,tar.gz} ./segmentation-models/
	cp -r ./data/segmented/flores/morsel ./segmentation-models/
	zip -r segmentation-models.zip ./segmentation-models/
	rm -R segmentation-models

prep: prepare_neen prepare_sien

prepare_neen:
	bash ./prepare-neen.sh

prepare_sien:
	bash ./prepare-sien.sh

download:
	bash ./download-data.sh

init:
	pip install -r requirements.txt
