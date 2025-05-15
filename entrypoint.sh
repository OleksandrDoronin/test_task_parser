#!/bin/bash

export ENV_FILE='.env'

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting the application..."
python main.py