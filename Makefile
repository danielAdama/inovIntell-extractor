PYTHON = python3
SCRIPT = main.py

all: run

run:
	$(PYTHON) $(SCRIPT) "$(PDF_PATH)"

clean:
	rm -rf __pycache__

.PHONY: all run install clean