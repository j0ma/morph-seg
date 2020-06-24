all: download prep flores

flores: create_flores_vocab train_morfessor

train_morfessor: train_morfessor_baseline train_flatcat

train_flatcat: \
	train_flatcat_ne \
	train_flatcat_si \
	train_flatcat_en

train_flatcat_en:
	echo "Training Morfessor Flatcat for EN"
	python ./src/train-flatcat.py \
		--lang en \
		-i ./data/raw/flores/flores.vocab.en.lowercase.withcounts \
		-o ./data/segmented/flores/en \
		--seed-segmentation-path ./data/segmented/flores/en/flores.vocab.en.lowercase.segmented.morfessor-baseline-batch-recursive \
		--construction-separator "<ConstSep>" \
		--model-type batch \
		--model-output-folder ./bin \
		--lowercase

train_flatcat_ne:
	echo "Training Morfessor Flatcat for NE"
	python ./src/train-flatcat.py \
		--lang ne \
		-i ./data/raw/flores/wiki_ne_en/flores.vocab.ne.lowercase.withcounts \
		-o ./data/segmented/flores/ne \
		--seed-segmentation-path ./data/segmented/flores/ne/flores.vocab.ne.lowercase.segmented.morfessor-baseline-batch-recursive \
		--construction-separator "<ConstSep>" \
		--model-type batch \
		--model-output-folder ./bin \
		--lowercase

train_flatcat_si:
	echo "Training Morfessor Flatcat for SI"
	python ./src/train-flatcat.py \
		--lang si \
		-i ./data/raw/flores/wiki_si_en/flores.vocab.si.lowercase.withcounts \
		-o ./data/segmented/flores/si \
		--seed-segmentation-path ./data/segmented/flores/si/flores.vocab.si.lowercase.segmented.morfessor-baseline-batch-recursive \
		--construction-separator "<ConstSep>" \
		--model-type batch \
		--model-output-folder ./bin \
		--lowercase

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
		--lowercase

create_flores_vocab: \
	create_flores_vocab_en \
	create_flores_vocab_ne \
	create_flores_vocab_si

create_flores_vocab_en:
	echo "Creating vocabulary for EN"
	bash ./src/create-flores-vocabulary.sh \
		--lang en \
		--raw-data-folder ./data/raw \
		--output-file ./data/raw/flores/flores.vocab.en.lowercase.withcounts \
		--with-counts

create_flores_vocab_ne:
	echo "Creating vocabulary for NE"
	bash ./src/create-flores-vocabulary.sh \
		--lang ne \
		--raw-data-folder ./data/raw \
		--output-file ./data/raw/flores/wiki_ne_en/flores.vocab.ne.lowercase.withcounts \
		--with-counts

create_flores_vocab_si:
	echo "Creating vocabulary for SI"
	bash ./src/create-flores-vocabulary.sh \
		--lang si \
		--raw-data-folder ./data/raw \
		--output-file ./data/raw/flores/wiki_si_en/flores.vocab.si.lowercase.withcounts \
		--with-counts

package_morfessor_models:
	mkdir -p morfessor-models
	cp ./bin/* morfessor-models/
	zip -r morfessor-models.zip ./morfessor-models
	rm -R morfessor-models

prep: prepare_neen prepare_sien

prepare_neen:
	bash ./prepare-neen.sh

prepare_sien:
	bash ./prepare-sien.sh

download:
	bash ./download-data.sh
