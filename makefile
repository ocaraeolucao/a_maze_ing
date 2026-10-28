PYTHON = python3
CONFIG = config.txt

.PHONY: install run debug clean lint lint-strict build

install:
	pip install .

run:
	$(PYTHON) a_maze_ing.py $(CONFIG)

debug:
	\$(PYTHON) -m pdb a_maze_ing.py \$(CONFIG)

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache build dist *.egg-info *.whl *.tar.gz

lint:
	flake8 .
	mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	flake8 .
	mypy --strict .

build:
	\$(PYTHON) -m build
	cp dist/*.whl .