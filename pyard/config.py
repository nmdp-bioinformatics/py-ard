# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Tuple


@dataclass
class ARDConfig:
    """Configuration class for ARD reduction settings"""

    reduce_serology: bool = True
    reduce_v2: bool = True
    reduce_3field: bool = True
    reduce_P: bool = True
    reduce_XX: bool = True
    reduce_MAC: bool = True
    reduce_shortnull: bool = True
    ping: bool = True
    verbose_log: bool = False
    ARS_as_lg: bool = False
    strict: bool = True
    ignore_allele_with_suffixes: Tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, config_dict: dict) -> "ARDConfig":
        """Create ARDConfig from dictionary"""
        if not config_dict:
            return cls()

        # Filter only valid fields
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_config = {k: v for k, v in config_dict.items() if k in valid_fields}

        return cls(**filtered_config)

    def to_dict(self) -> dict:
        """Convert ARDConfig to dictionary"""
        return {
            "reduce_serology": self.reduce_serology,
            "reduce_v2": self.reduce_v2,
            "reduce_3field": self.reduce_3field,
            "reduce_P": self.reduce_P,
            "reduce_XX": self.reduce_XX,
            "reduce_MAC": self.reduce_MAC,
            "reduce_shortnull": self.reduce_shortnull,
            "ping": self.ping,
            "verbose_log": self.verbose_log,
            "ARS_as_lg": self.ARS_as_lg,
            "strict": self.strict,
            "ignore_allele_with_suffixes": self.ignore_allele_with_suffixes,
        }

    @property
    def serology_enabled(self) -> bool:
        return self.reduce_serology

    @property
    def v2_enabled(self) -> bool:
        return self.reduce_v2

    @property
    def field3_enabled(self) -> bool:
        return self.reduce_3field

    @property
    def p_enabled(self) -> bool:
        return self.reduce_P

    @property
    def xx_enabled(self) -> bool:
        return self.reduce_XX

    @property
    def mac_enabled(self) -> bool:
        return self.reduce_MAC

    @property
    def shortnull_enabled(self) -> bool:
        return self.reduce_shortnull

    @property
    def ping_enabled(self) -> bool:
        return self.ping

    @property
    def verbose_enabled(self) -> bool:
        return self.verbose_log

    @property
    def ars_as_lg_enabled(self) -> bool:
        return self.ARS_as_lg

    @property
    def strict_enabled(self) -> bool:
        return self.strict
