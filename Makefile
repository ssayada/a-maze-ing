# Nom du programme principal
NAME = a_maze_ing.py
CONFIG = config.txt

# Commandes
PYTHON = python3
PIP = pip3

#Install dependencies
install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) $(NAME) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(NAME) $(CONFIG)

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info

lint:
	python3 -m flake8 .
	mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		 --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	flake8 .
	mypy --strict .

# Construction du package réutilisable (Chapter VI) [cite: 201, 203]
package:
	$(PYTHON) -m build

.PHONY: install run debug clean lint lint-strict package
