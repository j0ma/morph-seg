create_flores_vocab: \
	create_flores_vocab_en \
	create_flores_vocab_ne \
	create_flores_vocab_si

create_flores_vocab_en:
	cd ./src
	python create-flores-vocabulary.py \
		--lang en \
		--with-counts \
		--lowercase
	cd ..

create_flores_vocab_ne:
	cd ./src
	python create-flores-vocabulary.py \
		--lang ne \
		--with-counts \
		--lowercase
	cd ..

create_flores_vocab_si:
	cd ./src
	python create-flores-vocabulary.py \
		--lang si \
		--with-counts \
		--lowercase
	cd ..

prepare_neen:
	bash ./prepare_neen.sh

prepare_sien:
	bash ./prepare_sien.sh
