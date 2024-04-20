PYTHON = python3
PIP = $(PYTHON) -m pip
PROJECT_NAME = myproject
VENV_DIR = venv
REQUIREMENTS_FILE = requirements.txt

run: venv
	@$(VENV_DIR)/bin/python manage.py runserver

venv: 
	@$(PYTHON) -m venv $(VENV_DIR)
	@$(VENV_DIR)/bin/$(PIP) install -r $(REQUIREMENTS_FILE)
	
clean:
	rm -rf $(VENV_DIR)
