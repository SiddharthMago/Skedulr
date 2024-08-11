VENV_DIR := venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip
REQUIREMENTS := requirements.txt
SCRIPT := schedulerAPI.py

$(VENV_DIR)/bin/activate: 
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip

# Install the required packages
install: $(VENV_DIR)/bin/activate
	$(PIP) install -r $(REQUIREMENTS)

# Run the Python script
run: $(VENV_DIR)/bin/activate
	$(PYTHON) $(SCRIPT)

# Clean up the environment
clean:
	rm -rf $(VENV_DIR)

# Phony targets
.PHONY: install run clean
