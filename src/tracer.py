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

def _reflect(ray, r, c):
    """
    Use the same reflection rule already used in the original tracer.
    """
    fx = ray.x - c
    fy = ray.y - r

    if abs(fx - 0.5) < abs(fy - 0.5):
        ray.vx *= -1
    else:
        ray.vy *= -1
        
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
        - 'C' refract: continue straight and also generate one reflected ray.
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
                break
            if kind == 'A':
                _reflect(ray, r, c)
                continue
            if kind == 'C':
                #original ray continues straight through
                #create one reflected ray and trace it too
                new_ray = Ray(ray.x, ray.y, ray.vx, ray.vy)
                _reflect(new_ray, r, c)

                extra_steps = max(1, max_steps // 2)
                extra_path, extra_hits = trace_ray(new_ray, board, max_steps=extra_steps)

                for p in extra_path:
                    if p not in path:
                        path.append(p)

                for idx in extra_hits:
                    if idx not in hits:
                        hits.append(idx)

                continue
    return path, hits
