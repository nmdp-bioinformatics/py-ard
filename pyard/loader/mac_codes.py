import io
import sys
import zipfile
from urllib.error import URLError
from urllib.request import urlopen

from ..simple_table import Table


def load_mac_codes():
    """
    MAC files come in 2 different versions:

    Martin: when they’re printed, the first is better for encoding and the
    second is better for decoding. The entire list was maintained both as an
    Excel spreadsheet and also as a sybase database table. The Excel was the
    one that was printed and distributed.

        **==> numer.v3.txt <==**

        Sorted by the length and the values in the list
        ```
        "LAST UPDATED: 09/30/20"
        CODE	SUBTYPE

        AB	01/02
        AC	01/03
        AD	01/04
        AE	01/05
        AG	01/06
        AH	01/07
        AJ	01/08
        ```

        **==> alpha.v3.txt <==**

        Sorted by the code

        ```
        "LAST UPDATED: 10/01/20"
        *	CODE	SUBTYPE

            AA	01/02/03/05
            AB	01/02
            AC	01/03
            AD	01/04
            AE	01/05
            AF	01/09
            AG	01/06
        ```
    """
    mac_url = "https://hml.nmdp.org/mac/files/numer.v3.zip"
    try:
        response = urlopen(mac_url)
        zip_data = response.read()

        with zipfile.ZipFile(io.BytesIO(zip_data)) as zip_file:
            file_name = zip_file.namelist()[0]
            with zip_file.open(file_name) as file:
                lines = [line.decode("utf-8").strip() for line in file]
                data_lines = lines[3:]  # Skip first 3 header lines

                data_tuples = []
                for line in data_lines:
                    if line:
                        fields = line.split("\t")
                        if len(fields) >= 2:
                            data_tuples.append((fields[0], fields[1]))

                columns = ["Code", "Alleles"]
                return Table(data_tuples, columns)

    except URLError as e:
        print(f"Error downloading {mac_url}", e, file=sys.stderr)
        sys.exit(1)
