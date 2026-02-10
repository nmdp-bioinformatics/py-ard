#
#    py-ard
#    Copyright (c) 2023 Be The Match operated by National Marrow Donor Program. All Rights Reserved.
#
#    This library is free software; you can redistribute it and/or modify it
#    under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation; either version 3 of the License, or (at
#    your option) any later version.
#
#    This library is distributed in the hope that it will be useful, but WITHOUT
#    ANY WARRANTY; with out even the implied warranty of MERCHANTABILITY or
#    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
#    License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this library;  if not, write to the Free Software Foundation,
#    Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA.
#
#    > http://www.fsf.org/licensing/licenses/lgpl.html
#    > http://www.opensource.org/licenses/lgpl-license.php
#
from typing import Dict, List, Optional

from .exceptions import HLAToolsNotAvailableError

VALID_LOCI = [
    "A",
    "B",
    "C",
    "DRB1",
    "DRB3",
    "DRB4",
    "DRB5",
    "DQA1",
    "DQB1",
    "DPA1",
    "DPB1",
]

_bridge_instance = None


class HLAToolsBridge:
    """Bridge to the HLAtools R package via rpy2 for alignment data access."""

    def __init__(self, loci: Optional[List[str]] = None):
        """
        Initialize the bridge.

        Args:
            loci: List of loci to load when alignments are first requested.
                  Defaults to all standard HLA loci. Loading is deferred
                  until the first call to get_alignment().
        """
        self._loci = loci or VALID_LOCI
        self._alignment_cache: Dict[str, Dict[str, str]] = {}
        self._position_cache: Dict[str, Dict[int, int]] = {}
        self._r_initialized = False
        self._hlatools = None
        self._r_globalenv = None

    @property
    def is_available(self) -> bool:
        """Check if rpy2 and HLAtools are available without side effects."""
        try:
            import importlib

            importlib.import_module("rpy2")
        except ImportError:
            return False

        try:
            from rpy2.robjects.packages import isinstalled

            return isinstalled("HLAtools")
        except Exception:
            return False

    def _ensure_r_initialized(self):
        """Lazily initialize the R environment and load HLAtools."""
        if self._r_initialized:
            return

        if not self.is_available:
            raise HLAToolsNotAvailableError(
                "rpy2 and/or the HLAtools R package are not installed. "
                "Install with: pip install rpy2 && "
                "Rscript -e \"install.packages('HLAtools')\""
            )

        from rpy2.robjects.packages import importr
        from rpy2.robjects import globalenv

        self._hlatools = importr("HLAtools")
        self._r_globalenv = globalenv
        self._r_initialized = True

    def _ensure_alignments_loaded(self):
        """Load alignments into the R global environment if not already loaded."""
        self._ensure_r_initialized()

        from rpy2.robjects import r

        # Check if HLAalignments already exists in the R environment
        exists_result = r('exists("HLAalignments", envir = .GlobalEnv)')
        if exists_result[0]:
            return

        # Build loci vector for R
        from rpy2.robjects import StrVector

        loci_vec = StrVector(self._loci)
        result = self._hlatools.alignmentFull(loci=loci_vec, alignType="prot")
        self._r_globalenv["HLAalignments"] = result

    def get_alignment(self, locus: str) -> Dict[str, str]:
        """
        Get protein alignment data for a locus as allele->sequence dict.

        Args:
            locus: HLA locus name (e.g., "A", "DPB1", "DRB1").

        Returns:
            Dict mapping allele names to their full amino acid sequences.

        Raises:
            HLAToolsNotAvailableError: If R/HLAtools not available.
            ValueError: If locus is not valid.
        """
        if locus not in VALID_LOCI:
            raise ValueError(f"Invalid locus '{locus}'. Must be one of: {VALID_LOCI}")

        if locus in self._alignment_cache:
            return self._alignment_cache[locus]

        self._ensure_alignments_loaded()

        from rpy2.robjects import r
        import rpy2.robjects as ro

        # Access the protein alignment data frame for this locus
        df = r(f"HLAalignments$prot${locus}")

        if df is ro.NULL or df is None:
            self._alignment_cache[locus] = {}
            return {}

        alignment_dict = self._dataframe_to_dict(df)
        self._alignment_cache[locus] = alignment_dict
        return alignment_dict

    def _dataframe_to_dict(self, df) -> Dict[str, str]:
        """Convert an HLAtools alignment R data frame to allele->sequence dict."""
        import rpy2.robjects as ro
        from rpy2.robjects import pandas2ri
        from rpy2.robjects.conversion import localconverter

        with localconverter(ro.default_converter + pandas2ri.converter):
            pdf = ro.conversion.get_conversion().rpy2py(df)

        col_names = list(pdf.columns)

        # Metadata columns: locus, allele, trimmed_allele, allele_name
        # Position columns (IMGT positions) start at index 4
        seq_cols = col_names[4:]

        alignment_dict = {}
        for _, row in pdf.iterrows():
            allele_name = str(row["allele_name"])
            sequence = "".join(str(row[col]) for col in seq_cols)
            # Replace "." (absent/gap) with "" to get clean sequence
            sequence = sequence.replace(".", "")
            alignment_dict[allele_name] = sequence

        return alignment_dict

    def get_sequence(self, allele: str) -> Optional[str]:
        """
        Get the protein sequence for a single allele.

        Tries exact match first, then progressively shorter prefixes
        (e.g., 4-field -> 3-field -> 2-field).

        Args:
            allele: Full allele name (e.g., "DPB1*04:01:01:01").

        Returns:
            Amino acid sequence string, or None if not found.
        """
        if not allele or "*" not in allele:
            return None

        locus = allele.split("*")[0]
        alignment = self.get_alignment(locus)

        if not alignment:
            return None

        # Exact match
        if allele in alignment:
            return alignment[allele]

        # Prefix fallback: try progressively shorter field counts
        parts = allele.split(":")
        for i in range(len(parts) - 1, 0, -1):
            prefix = ":".join(parts[:i])
            for full_allele in alignment:
                if full_allele.startswith(prefix):
                    return alignment[full_allele]

        return None

    def compare_sequences(self, allele1: str, allele2: str) -> Dict:
        """
        Compare two alleles using HLAtools compareSequences().

        Args:
            allele1: First allele name.
            allele2: Second allele name.

        Returns:
            Dict with keys 'identical' (bool), and if not identical,
            'positions' (list of int/str position labels) and
            'allele1_residues'/'allele2_residues' (list of residues).
        """
        self._ensure_alignments_loaded()

        from rpy2.robjects import StrVector
        import rpy2.robjects as ro

        alleles_vec = StrVector([allele1, allele2])
        result = self._hlatools.compareSequences("prot", alleles_vec)

        # If sequences are identical, HLAtools returns a character message
        if isinstance(result, ro.vectors.StrVector):
            return {"identical": True, "message": str(result[0])}

        # Otherwise it's a data frame with differing positions
        from rpy2.robjects import pandas2ri
        from rpy2.robjects.conversion import localconverter

        with localconverter(ro.default_converter + pandas2ri.converter):
            pdf = ro.conversion.get_conversion().rpy2py(result)

        col_names = list(pdf.columns)
        position_cols = [c for c in col_names if c != "allele_name"]

        positions = []
        for col in position_cols:
            try:
                positions.append(int(col))
            except ValueError:
                try:
                    positions.append(float(col))
                except ValueError:
                    positions.append(col)

        rows = pdf.values.tolist()
        return {
            "identical": False,
            "positions": positions,
            "allele1_residues": [
                str(rows[0][i + 1]) for i in range(len(position_cols))
            ],
            "allele2_residues": [
                str(rows[1][i + 1]) for i in range(len(position_cols))
            ],
        }

    def get_position_mapping(self, locus: str) -> Dict[int, int]:
        """
        Get mapping from 0-based sequence index to IMGT position number.

        HLAtools data frames have IMGT positions as column headers,
        so this directly solves the leader/mature boundary problem
        (negative positions = leader, positive = mature protein).

        Args:
            locus: HLA locus name.

        Returns:
            Dict mapping 0-based sequence index to IMGT position number.
        """
        if locus not in VALID_LOCI:
            raise ValueError(f"Invalid locus '{locus}'. Must be one of: {VALID_LOCI}")

        if locus in self._position_cache:
            return self._position_cache[locus]

        self._ensure_alignments_loaded()

        from rpy2.robjects import r

        df = r(f"HLAalignments$prot${locus}")
        if df is None:
            return {}

        from rpy2.robjects import pandas2ri
        from rpy2.robjects.conversion import localconverter
        import rpy2.robjects as ro

        with localconverter(ro.default_converter + pandas2ri.converter):
            pdf = ro.conversion.get_conversion().rpy2py(df)

        col_names = list(pdf.columns)
        position_cols = col_names[4:]  # Skip metadata columns

        mapping = {}
        seq_index = 0
        for col in position_cols:
            if col.startswith("E."):
                continue
            try:
                imgt_pos = int(col)
            except ValueError:
                try:
                    imgt_pos = float(col)
                except ValueError:
                    continue
            mapping[seq_index] = imgt_pos
            seq_index += 1

        self._position_cache[locus] = mapping
        return mapping

    def clear_cache(self):
        """Reset all cached alignment and position data."""
        self._alignment_cache.clear()
        self._position_cache.clear()


def get_bridge(loci: Optional[List[str]] = None) -> HLAToolsBridge:
    """Get or create the singleton HLAToolsBridge instance."""
    global _bridge_instance
    if _bridge_instance is None:
        _bridge_instance = HLAToolsBridge(loci=loci)
    return _bridge_instance


def load_protein_alignment(locus: str) -> Dict[str, str]:
    """
    Load protein alignment for a locus via HLAtools.

    Drop-in replacement for the notebook's load_protein_alignment_enhanced().

    Args:
        locus: HLA locus name (e.g., "DPB1").

    Returns:
        Dict mapping allele names to amino acid sequences.
    """
    bridge = get_bridge()
    return bridge.get_alignment(locus)
