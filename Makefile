
# Makefile for nlm-connect

.PHONY: install run clean

install:
	pip install -r requirements.txt

run:
	python src/main.py --sync --output ./transcripts

clean:
	rm -rf __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +
