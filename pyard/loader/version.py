import sys
from urllib.error import URLError

from ..loader import IMGT_HLA_URL


def load_latest_version():
    from urllib.request import urlopen

    version_txt = f"{IMGT_HLA_URL}/Latest/release_version.txt"
    try:
        response = urlopen(version_txt)
    except URLError as e:
        print(f"Error downloading {version_txt}", e, file=sys.stderr)
        sys.exit(1)

    version = 0
    for line in response:
        l = line.decode("utf-8")
        if l.find("version:") != -1:
            # Version line looks like
            # # version: IPD-IMGT/HLA 3.51.0
            version = l.split()[-1].replace(".", "")
    return version
