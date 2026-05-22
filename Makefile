.PHONY: install run debug clean lint lint-strict

# Имя основного скрипта
MAIN_SCRIPT = a_maze_ing.py
CONFIG_FILE = config.txt

install:
	pip install -r requirements.txt || echo "No requirements.txt found, skipping dependency installation."

run:
	python3 $(MAIN_SCRIPT) $(CONFIG_FILE)

debug:
	python3 -m pdb $(MAIN_SCRIPT) $(CONFIG_FILE)

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict