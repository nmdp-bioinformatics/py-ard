# GitHub URL where IPD/IMGT-HLA files are downloaded.
import os

DEFAULT_IMGT_HLA_URL = "https://raw.githubusercontent.com/ANHIG/IMGTHLA/"
IMGT_HLA_URL = os.getenv("IMGT_HLA_URL", DEFAULT_IMGT_HLA_URL)
if IMGT_HLA_URL != DEFAULT_IMGT_HLA_URL:
    print(f"Using URL: {IMGT_HLA_URL}")
