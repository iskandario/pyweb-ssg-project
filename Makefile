.PHONY: build serve clean

build:
	mkdocs build --strict

serve:
	mkdocs serve

clean:
	rm -rf site
