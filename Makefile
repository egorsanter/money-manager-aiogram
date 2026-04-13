all:
ifeq ($(OS),Windows_NT)
	python -m venv .venv
	.venv\Scripts\pip.exe install -r requirements.txt
	.venv\Scripts\python.exe main.py
else
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
	.venv/bin/python main.py
endif