.PHONY: install install-dev run migrate all

VENV = .venv

install:
ifeq ($(OS),Windows_NT)
	python -m venv $(VENV)
	$(VENV)\Scripts\pip.exe install -r requirements.txt
else
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt
endif

install-dev: install
ifeq ($(OS),Windows_NT)
	$(VENV)\Scripts\pip.exe install -r requirements-dev.txt
else
	$(VENV)/bin/pip install -r requirements-dev.txt
endif

migrate:
ifeq ($(OS),Windows_NT)
	$(VENV)\Scripts\alembic.exe upgrade head
else
	$(VENV)/bin/alembic upgrade head
endif

run:
ifeq ($(OS),Windows_NT)
	$(VENV)\Scripts\python.exe main.py
else
	$(VENV)/bin/python main.py
endif

all: install migrate run