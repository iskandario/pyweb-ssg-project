.PHONY: prepare build serve clean

prepare:
	python scripts/run_experiment.py

build: prepare
	mkdocs build --strict

serve: prepare
	mkdocs serve

clean:
	rm -rf site docs/generated

