#Program name
NAME = a_maze_ing.py
CONFIG = config.txt

# Commandes
PYTHON = python3
PIP = pip
MAZEGEN = mazegen-1.0.0.tar.gz

#Install dependencies
install:
	$(PYTHON) -m $(PIP) install --force-reinstall $(MAZEGEN)

run:
	$(PYTHON) $(NAME) $(CONFIG)

clean:
	rm -rf __pycache__ maze_gen/__pycache__ ui/__pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache maze_gen/.mypy_cache ui/mypy_cache

lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		 --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	$(PYTHON) flake8 .
	mypy --strict .

debug:
	$(PYTHON) -m pdb a_maze_ing.py config.txt

package:
	$(PYTHON) -m build

.PHONY: install run debug clean lint lint-strict package
