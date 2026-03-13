# HLAtools Alignment Demo

Donor-recipient compatibility analysis using real amino acid sequences from the HLAtools R package.

## Quick Start

```bash
git clone https://github.com/cbumby17/py-ard.git
cd py-ard
git checkout feature/hlatools-alignment-bridge
./demos/setup.sh
```

Then launch the notebook:

```bash
source demos/.venv/bin/activate
jupyter notebook demos/Standalone_Enhanced_Demo.ipynb
```

Select the **py-ard Demo** kernel when prompted.

## Prerequisites

- **Python 3.9+**
- **R** (>= 3.6) &mdash; `brew install r` if not already installed
- **HLAtools R package** &mdash; installed automatically by `setup.sh`

## What the Setup Script Does

1. Creates a local virtual environment at `demos/.venv/`
2. Installs Python dependencies: `rpy2`, `pandas`, `jupyter`, `ipykernel`
3. Installs `py-ard` in development mode from the repo
4. Registers a Jupyter kernel named "py-ard Demo"
5. Installs the HLAtools R package if not already present

## Manual Setup (if you prefer)

```bash
python3 -m venv demos/.venv
source demos/.venv/bin/activate
pip install rpy2 pandas jupyter ipykernel
pip install -e .
python -m ipykernel install --user --name py-ard-demo --display-name "py-ard Demo"
Rscript -e 'install.packages("HLAtools")'
jupyter notebook demos/Standalone_Enhanced_Demo.ipynb
```

## What the Notebook Demonstrates

- Loading protein alignment data via HLAtools (with fallback to direct IMGT parsing)
- Single allele amino acid sequence comparison
- IMGT position mapping with accurate leader/mature boundary classification
- Donor-recipient genotype compatibility analysis across all allele combinations
- CSV export with IMGT positions and sequence region annotations
- Multi-locus support (A, B, C, DRB1, DPB1)

Edit the genotype strings in Tests 2 and 4 to try different allele combinations.
