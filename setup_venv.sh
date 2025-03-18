#!/bin/bash

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

echo "Setup complete! To activate the virtual environment in the future, run:"
echo "source venv/bin/activate" 