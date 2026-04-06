# -*- coding: utf-8 -*-
"""
Ray
"""


import math
from typing import Tuple


class Ray:
    def __init__(self, x: float, y: float, vx: float, vy: float):
        if vx == 0 and vy == 0:
            raise ValueError("Ray direction cannot be zero")
        norm = math.hypot(vx, vy)
        self.x = float(x)
        self.y = float(y)
        self.vx = vx / norm
        self.vy = vy / norm

    def step(self, dist: float = 0.25):
        self.x += self.vx * dist
        self.y += self.vy * dist

    def pos(self) -> Tuple[float, float]:
        return (self.x, self.y)
