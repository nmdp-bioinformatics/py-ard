# -*- coding: utf-8 -*-

from typing import Iterable, TYPE_CHECKING

from .. import db

if TYPE_CHECKING:
    from ..ard import ARD


class SerologyHandler:
    """Handles serology-related operations"""

    def __init__(self, ard_instance: "ARD"):
        self.ard = ard_instance

    def is_serology(self, allele: str) -> bool:
        """Check if allele is valid serology"""
        if "*" in allele or ":" in allele:
            return False
        return allele in self.ard.valid_serology_set

    def get_alleles_from_serology(self, serology: str) -> Iterable[str]:
        """Get alleles corresponding to serology"""
        alleles = db.serology_to_alleles(self.ard.db_connection, serology)
        return set(filter(self.ard._is_allele_in_db, alleles))

    def find_broad_splits(self, allele: str) -> tuple:
        """Find broad/splits for serology"""
        return self.ard.serology_mapping.find_splits(allele)

    def find_associated_antigen(self, serology: str) -> str:
        """Find associated antigen for serology"""
        return self.ard.serology_mapping.find_associated_antigen(serology)

    def find_xx_from_serology(self, serology: str) -> str:
        """Find XX code from serology"""
        if self.is_serology(serology):
            return db.find_xx_for_serology(self.ard.db_connection, serology)
        from ..exceptions import InvalidAlleleError

        raise InvalidAlleleError(f"{serology} is not a valid serology")
