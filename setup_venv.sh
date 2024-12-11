#!/bin/bash

# Setting the name of the virtual environment directory
VENV_DIR="weather_dashboard_venv"
REQUIREMENTS_FILE="requirements.txt"  

# Checking if the virtual environment already exists
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment for weather dashboard app..."
  python3 -m venv "$VENV_DIR"  # Create the virtual environment

  # Activating the virtual environment
  source "$VENV_DIR/bin/activate"

  # Checking if the requirements file exists and install dependencies
  if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing dependencies from $REQUIREMENTS_FILE..."
    pip install --no-cache-dir -r "$REQUIREMENTS_FILE"  # Installing dependencies
  else
    echo "Error: $REQUIREMENTS_FILE not found."
    exit 1  # Exit if requirements.txt is non-existent
  fi
else
  # Activating the existing virtual environment
  source "$VENV_DIR/bin/activate"
  echo "Virtual environment already exists. Activated."
fi

# Confirming that the environment is set up
echo "Weather Dashboard app environment is ready!"
