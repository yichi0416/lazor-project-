# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:59:21 2026

@author: zpaul
"""

from typing import List, Tuple, Optional
from .board import Board
from .solver_utils import check_board_solution


def solve_bruteforce(board: Board, positions: List[Tuple[int, int]] = None, idx: int = 0) -> Optional[Board]:
    """
    Very simple recursive backtracking solver.
    Returns a Board object with placed blocks if solution found, else None.
    Note: this mutates the board in place for efficiency and backtracks on removal.
    """
    if positions is None:
        positions = board.allowed[:]
    # quick check
    if check_board_solution(board):
        return board
    if idx >= len(positions):
        return None
    r, c = positions[idx]
    # option 1: leave empty
    sol = solve_bruteforce(board, positions, idx+1)
    if sol is not None:
        return sol
    # option 2: try each available block type
    for kind in list(board.available_blocks.keys()):
        if board.available_blocks.get(kind, 0) <= 0:
            continue
        ok = board.place_block(r, c, kind)
        if not ok:
            continue
        sol = solve_bruteforce(board, positions, idx+1)
        if sol is not None:
            return sol
        # backtrack
        board.remove_block(r, c)
    return None
