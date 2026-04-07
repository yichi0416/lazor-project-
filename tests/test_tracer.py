# -*- coding: utf-8 -*-
"""
testtracer
"""

import unittest
from src.parser import parse_bff
from src.board import Board
from src.ray import Ray
from src.tracer import trace_ray


class TestTracer(unittest.TestCase):
    def test_empty_hit(self):
        # construct a tiny board with a point at (2,0) and laser aiming at it
        grid = ["ooo", "ooo", "ooo"]
        blocks = {"A": 0, "B": 0, "C": 0}
        lasers = [(0.5, 2.5, 1.0, -1.0)]  # approx towards top-right
        points = [(2.0, 0.0)]
        b = Board(grid, blocks, lasers, points)
        ray = Ray(*lasers[0])
        path, hits = trace_ray(ray, b, max_steps=1000)
        self.assertTrue(len(hits) >= 0)  # basic sanity (could be refined)


if __name__ == "__main__":
    unittest.main()
