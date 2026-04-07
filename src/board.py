# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:52:04 2026

@author: zpaul
"""

from typing import List, Tuple, Dict, Optional
from .block import Block


class Board:
    def __init__(self, grid: List[str], available_blocks: Dict[str, int], lasers: List[Tuple[float, float, float, float]], points: List[Tuple[float, float]]):
        self.grid = grid[:]  # list[str], top-to-bottom rows
        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) if self.rows > 0 else 0
        # cells maps (r,c) to Block or None
        self.cells: Dict[Tuple[int, int], Optional[Block]] = {}
        self.allowed: List[Tuple[int, int]] = []
        # populate cells
        for r, row in enumerate(self.grid):
            for c, ch in enumerate(row):
                if ch in ('o', 'O'):
                    self.cells[(r, c)] = None
                    self.allowed.append((r, c))

                elif isinstance(ch,Block):
                    self.cells[(r,c)] = ch
                    
                elif ch in ('A', 'B', 'C', 'F'):  # fixed letters (F treated as opaque fixed custom)
                    kind = ch
                    self.cells[(r, c)] = Block(kind=kind, fixed=True)
                    
                else:
                    # 'x' or '.' or other empty space: no block allowed here, represent as None but not allowed
                    self.cells[(r, c)] = None
        self.available_blocks = available_blocks.copy()
        self.lasers = lasers[:]    # list of (x,y,vx,vy)
        self.points = points[:]    # list of (x,y)

    def place_block(self, r: int, c: int, kind: str) -> bool:
        if (r, c) not in self.cells:
            return False
        cur = self.cells[(r, c)]
        if cur is not None and getattr(cur, "fixed", False):
            return False
        if self.available_blocks.get(kind, 0) <= 0:
            return False
        # place
        self.cells[(r, c)] = Block(kind=kind, fixed=False)
        self.available_blocks[kind] -= 1
        return True

    def remove_block(self, r: int, c: int) -> Optional[str]:
        if (r, c) not in self.cells:
            return None
        cur = self.cells[(r, c)]
        if cur is None:
            return None
        if cur.fixed:
            return None
        kind = cur.kind
        self.cells[(r, c)] = None
        self.available_blocks[kind] = self.available_blocks.get(kind, 0) + 1
        return kind

    def get_block(self, r: int, c: int):
        return self.cells.get((r, c))

    def pretty_print(self):
        print("Board:")
        for r in range(self.rows):
            row = ''
            for c in range(self.cols):
                b = self.cells.get((r, c))
                if b is None:
                    row += self.grid[r][c]
                else:
                    row += b.kind
            print(row)
