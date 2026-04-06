# -*- coding: utf-8 -*-
"""
Tracer
"""

import math
from typing import List, Tuple
from .ray import Ray
from .board import Board

EPS_POINT = 0.25  # how close to a target counts as hit


def hit_point(x: float, y: float, points: List[Tuple[float, float]], eps: float = EPS_POINT):
    hits = []
    for idx, (px, py) in enumerate(points):
        if math.hypot(x-px, y-py) <= eps:
            hits.append(idx)
    return hits


def trace_ray(ray: Ray, board: Board, max_steps: int = 2000):
    """
    Trace a single ray through the board.
    Returns:
      - path: list of (x,y) points visited (for visualization)
      - hit_point_indices: list of indices of points (board.points) this ray hit in order
    Simplified physics:
      - We advance the ray in small steps and check the cell it is in via int(y), int(x)
      - Block types:
        - 'B' opaque: stop ray.
        - 'A' reflect: flip vx or vy depending on approach (heuristic).
        - 'C' refract: pass-through (no split) in this starter implementation.
    """
    path = []
    hits = []
    for _ in range(max_steps):
        ray.step()
        x, y = ray.pos()
        path.append((x, y))
        # check for target hits
        h = hit_point(x, y, board.points)
        if h:
            for idx in h:
                if idx not in hits:
                    hits.append(idx)
            # Do not return immediately — allow multiple hits by same ray
        # check board bounds
        if x < 0 or y < 0 or x >= board.cols or y >= board.rows:
            break
        # check cell
        r = int(y)
        c = int(x)
        if (r, c) in board.cells:
            b = board.get_block(r, c)
            if b is None:
                continue
            kind = b.kind
            if kind == 'B':
                # opaque: stop
                break
            if kind == 'A':
                # reflection heuristic:
                # determine which axis is dominant in approach by looking at fractional parts
                # flip the velocity component that aligns with larger approach
                # (This is a simplification; exact physics requires edge intersection.)
                fx = x - c
                fy = y - r
                # decide flip based on which fractional part is closer to 0.5 (i.e., crossing an edge)
                if abs(fx - 0.5) < abs(fy - 0.5):
                    # more horizontal crossing => flip vx
                    ray.vx *= -1
                else:
                    ray.vy *= -1
                # continue after bounce
                continue
            if kind == 'C':
                # refract: starter behavior = pass through (no change)
                continue
    return path, hits
