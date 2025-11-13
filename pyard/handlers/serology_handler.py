# -*- coding: utf-8 -*-

from typing import Iterable, TYPE_CHECKING

from .. import db

if TYPE_CHECKING:
    from ..ard import ARD


class SerologyHandler:
    """Handles serology-related operations

    Serology refers to the historical method of HLA typing using antibodies
    to detect cell surface antigens. This class provides functionality to:
    - Validate serological typing designations
    - Convert between serology and molecular allele representations
    - Handle broad/split antigen relationships
    """

    def __init__(self, ard_instance: "ARD"):
        """Initialize the SerologyHandler with an ARD instance

        Args:
            ard_instance: The main ARD object for database access and serology mappings
        """
        self.ard = ard_instance

    def is_serology(self, allele: str) -> bool:
        """Check if allele is valid serology

        Serological designations are simple alphanumeric codes without
        the '*' or ':' characters used in molecular typing (e.g., 'A1', 'B27', 'DR4').

        Args:
            allele: String to check for serology format

        Returns:
            True if the string is a valid serological designation, False otherwise
        """
        # Serology codes don't contain molecular typing delimiters
        if "*" in allele or ":" in allele:
            return False
        # Check against the set of valid serology codes in the database
        return allele in self.ard.valid_serology_set

    def get_alleles_from_serology(self, serology: str) -> Iterable[str]:
        """Get alleles corresponding to serology

        Converts a serological designation to its corresponding molecular alleles.
        Multiple alleles may correspond to a single serology due to the lower
        resolution of serological typing methods.

        Args:
            serology: Serological designation (e.g., 'A1', 'B27')

        Returns:
            Set of molecular alleles that correspond to the serology,
            filtered to only include alleles present in the current database
        """
        # Query database for alleles associated with this serology
        alleles = db.serology_to_alleles(self.ard.db_connection, serology)
        # Filter to only include alleles that exist in current database
        return set(filter(self.ard._is_allele_in_db, alleles))

    def find_broad_splits(self, allele: str) -> tuple:
        """Find broad/splits for serology

        In serology, some antigens are 'broad' (general) while others are
        'splits' (more specific subdivisions). This method finds the
        broad/split relationships for a given antigen.

        Args:
            allele: Serological or molecular designation

        Returns:
            Tuple containing broad and split antigen information
        """
        return self.ard.serology_mapping.find_splits(allele)

    def find_associated_antigen(self, serology: str) -> str:
        """Find associated antigen for serology

        Some serological designations have associated or related antigens.
        This method finds the primary antigen associated with a given serology.

        Args:
            serology: Serological designation

        Returns:
            Associated antigen designation
        """
        return self.ard.serology_mapping.find_associated_antigen(serology)

    def find_xx_from_serology(self, serology: str) -> str:
        """Find XX code from serology

        XX codes represent groups of alleles that share serological reactivity.
        This method finds the XX code that corresponds to a given serology.

        Args:
            serology: Serological designation to look up

        Returns:
            XX code corresponding to the serology

        Raises:
            InvalidAlleleError: If the serology is not valid
        """
        if self.is_serology(serology):
            return db.find_xx_for_serology(self.ard.db_connection, serology)
        from ..exceptions import InvalidAlleleError

        raise InvalidAlleleError(f"{serology} is not a valid serology")
