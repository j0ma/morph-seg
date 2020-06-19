train_morfessor_baseline: \
	train_morfessor_baseline_si \
	train_morfessor_baseline_ne \
	train_morfessor_baseline_en

train_morfessor_baseline_en:
	python ./src/train-morfessor-baseline.py \
		--lang en \
		-i ./data/raw/flores/flores.vocab.en.lowercase.withcounts \
		-o ./data/segmented/flores/en \
		--model-type batch-recursive \
		--model-output-folder ./bin \
		--lowercase

train_morfessor_baseline_ne:
	python ./src/train-morfessor-baseline.py \
		--lang ne \
		-i ./data/raw/flores/wiki_ne_en/flores.vocab.ne.lowercase.withcounts \
		-o ./data/segmented/flores/ne \
		--model-type batch-recursive \
		--model-output-folder ./bin \
		--lowercase

train_morfessor_baseline_si:
	python ./src/train-morfessor-baseline.py \
		--lang si \
		-i ./data/raw/flores/wiki_si_en/flores.vocab.si.lowercase.withcounts \
		-o ./data/segmented/flores/ne \
		--model-type batch-recursive \
		--model-output-folder ./bin \
		--lowercase

create_flores_vocab: \
	create_flores_vocab_en \
	create_flores_vocab_ne \
	create_flores_vocab_si

create_flores_vocab_en:
	python ./src/create-flores-vocabulary.py \
		--lang en \
		--raw-data-folder ./data/raw \
		--with-counts

create_flores_vocab_ne:
	python ./src/create-flores-vocabulary.py \
		--lang ne \
		--raw-data-folder ./data/raw \
		--with-counts

create_flores_vocab_si:
	python ./src/create-flores-vocabulary.py \
		--lang si \
		--raw-data-folder ./data/raw \
		--with-counts

prepare_neen:
	bash ./prepare_neen.sh

prepare_sien:
	bash ./prepare_sien.sh
