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
