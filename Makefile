.PHONY: venv install run debug clean fclean build package lint lint-strict

# Main script name
PYTHON ?= python3
VENV = venv
VENV_PYTHON = $(VENV)/bin/python
VENV_PIP = $(VENV_PYTHON) -m pip
DEPS_STAMP = $(VENV)/.deps-installed
MAIN_SCRIPT = a_maze_ing.py
CONFIG_FILE = config.txt

venv: $(VENV_PYTHON)

$(VENV_PYTHON):
	$(PYTHON) -m venv $(VENV)

install: $(DEPS_STAMP)

$(DEPS_STAMP): $(VENV_PYTHON)
	$(VENV_PIP) install --upgrade pip build setuptools wheel flake8 mypy
	test ! -f requirements.txt || $(VENV_PIP) install -r requirements.txt
	touch $(DEPS_STAMP)

run: venv
	$(VENV_PYTHON) $(MAIN_SCRIPT) $(CONFIG_FILE)

debug: venv
	$(VENV_PYTHON) -m pdb $(MAIN_SCRIPT) $(CONFIG_FILE)

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache build dist *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +

fclean: clean
	rm -rf $(VENV)

build: install
	$(VENV_PYTHON) -m build --no-isolation
	cp dist/mazegen-* .

package: build

lint: install
	$(VENV)/bin/flake8 . --exclude=$(VENV),build,dist
	$(VENV_PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: install
	$(VENV)/bin/flake8 .
	$(VENV_PYTHON) -m mypy . --strict
