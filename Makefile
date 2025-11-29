# Makefile for the BlinkSense project.

# Variables
.PHONY: all venv install test
VENV_DIR := .venv

ifeq ($(OS),Windows_NT)
	PYTHON := $(VENV_DIR)/Scripts/python.exe
	PIP := $(VENV_DIR)/Scripts/pip.exe
else
	PYTHON := $(VENV_DIR)/bin/python
	PIP := $(VENV_DIR)/bin/pip
endif


all: test

venv:
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV_DIR)

install: venv
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt

test: install
	@echo "Running tests..."
	$(PYTHON) .listener

sender: install
	@echo "Running tests..."
	$(PYTHON) .listener

listener: install
	@echo "Running tests..."
	$(PYTHON) .listener