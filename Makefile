# Set the virtual environment name
VENV_NAME = pong

# Python interpreter
PYTHON = python3

# Set the virtual environment activation command based on the operating system
ifeq ($(OS),Windows_NT)
    ACTIVATE = $(VENV_NAME)\Scripts\activate
    DEACTIVATE = deactivate
    RM = rmdir /s /q
else
    ACTIVATE = . $(VENV_NAME)/bin/activate
    DEACTIVATE = deactivate
    RM = rm -rf
endif

# Default target: setup
setup: $(VENV_NAME)/bin/activate
	# Activate virtual environment and install dependencies
	@$(ACTIVATE) && pip install -r requirements.txt

$(VENV_NAME)/bin/activate: requirements.txt
	# Create virtual environment
	@$(PYTHON) -m venv $(VENV_NAME)
	# Touch activate file to ensure it is newer than requirements.txt
	@touch $(VENV_NAME)/bin/activate

# Target: clean
clean:
	# Deactivate virtual environment and remove it
	@$(DEACTIVATE) || true
	@$(RM) $(VENV_NAME)

.PHONY: setup clean