PYTHON = python3
SCRIPT = main.py

all: run

run:
	$(PYTHON) $(SCRIPT) "$(PDF_PATH)"

# Clean target (optional, if you have any temporary files to clean up)
clean:
	rm -rf __pycache__

.PHONY: all run install clean