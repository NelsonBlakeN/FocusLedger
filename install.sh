#!/usr/bin/env bash
# install.sh: Set up a local Python environment and install dependencies for FocusLedger
set -e

ENV_DIR=".venv"

# Create .venv if it doesn't exist
if [ ! -d "$ENV_DIR" ]; then
    python3 -m venv "$ENV_DIR"
    echo "Created virtual environment in $ENV_DIR"
fi

# Activate the environment
source "$ENV_DIR/bin/activate"
echo "Activated virtual environment."

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

echo "\nSetup complete! To activate the environment later, run:"
echo "  source $ENV_DIR/bin/activate"
echo "To run the app:"
echo "  python focusledger/app.py"
