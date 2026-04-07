# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:51:02 2026

@author: zpaul
"""

# src/block.py
from dataclasses import dataclass


@dataclass
class Block:
    kind: str    # 'A' reflect, 'B' opaque, 'C' refract
    fixed: bool = False

    def __repr__(self):
        return f"Block(kind={self.kind}, fixed={self.fixed})"
