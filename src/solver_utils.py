# -*- coding: utf-8 -*-
"""
Solver_utils
"""

from .board import Board
from .ray import Ray
from .tracer import trace_ray


def check_board_solution(board: Board) -> bool:
    """
    Return True if all target points are hit by at least one laser ray from the board's lasers.
    Uses trace_ray on each laser. Marks points hit when traced.
    """
    n_pts = len(board.points)
    if n_pts == 0:
        return True
    hit_mask = [False] * n_pts
    for lx,ly,vx,vy in board.lasers:
        ray = Ray(lx, ly, vx, vy)
        _, hits = trace_ray(ray, board)
        for idx in hits:
            hit_mask[idx] = True
        if all(hit_mask):
            return True
    return all(hit_mask)
