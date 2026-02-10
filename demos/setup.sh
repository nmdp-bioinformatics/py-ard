#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=== py-ard HLAtools Demo Setup ==="
echo ""

# Check for R
if ! command -v R &>/dev/null; then
    echo "ERROR: R is not installed. Install with: brew install r"
    exit 1
fi
echo "R found: $(R --version 2>&1 | head -1)"

# Check for Python 3
if ! command -v python3 &>/dev/null; then
    echo "ERROR: Python 3 is not installed."
    exit 1
fi
echo "Python found: $(python3 --version)"

# Create virtual environment
VENV_DIR="$SCRIPT_DIR/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo ""
    echo "Creating virtual environment at $VENV_DIR ..."
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
echo "Using venv: $VENV_DIR"

# Install Python dependencies
echo ""
echo "Installing Python dependencies ..."
pip install --quiet --upgrade pip
pip install --quiet rpy2 pandas jupyter ipykernel

# Install py-ard in development mode
echo "Installing py-ard (dev mode) ..."
pip install --quiet -e "$PROJECT_ROOT"

# Register Jupyter kernel
python -m ipykernel install --user --name py-ard-demo --display-name "py-ard Demo"

# Install HLAtools R package if needed
echo ""
echo "Checking for HLAtools R package ..."
Rscript -e '
if (!requireNamespace("HLAtools", quietly = TRUE)) {
    cat("Installing HLAtools ...\n")
    install.packages("HLAtools", repos = "https://cloud.r-project.org")
} else {
    cat("HLAtools already installed:", as.character(packageVersion("HLAtools")), "\n")
}
'

echo ""
echo "=== Setup complete ==="
echo ""
echo "To launch the notebook:"
echo "  source $VENV_DIR/bin/activate"
echo "  jupyter notebook $SCRIPT_DIR/Standalone_Enhanced_Demo.ipynb"
echo ""
echo "Make sure to select the 'py-ard Demo' kernel in the notebook."
