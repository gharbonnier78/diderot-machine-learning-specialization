PYTHON ?= python3
VERSION := 0.1.0
BOOK := diderot-ml-specialization-v$(VERSION)

.PHONY: setup figures book test verify clean archive

setup:
	$(PYTHON) -m pip install -r requirements.txt

figures:
	mkdir -p tmp/matplotlib
	MPLCONFIGDIR=tmp/matplotlib PYTHONPATH=src $(PYTHON) -m diderot_mls.gaussian --output book/figures/gaussian-comparison.pdf

book: figures
	mkdir -p book/build output/pdf
	cd book && pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
	cd book && pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
	cp book/build/main.pdf output/pdf/$(BOOK).pdf

test:
	mkdir -p tmp/matplotlib
	MPLCONFIGDIR=tmp/matplotlib PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

verify: book test
	pdfinfo output/pdf/$(BOOK).pdf

archive:
	git archive --format=zip --output=../$(BOOK)-source.zip HEAD

clean:
	rm -rf book/build tmp/pdfs/*
