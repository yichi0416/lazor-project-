# -*- coding: utf-8 -*-
"""
testsolver
"""

import unittest
from src.board import Board
from src.solver import solve_bruteforce


class TestSolver(unittest.TestCase):
    def test_trivial_no_blocks(self):
        grid = ["ooo", "ooo"]
        blocks = {"A": 0, "B": 0, "C": 0}
        lasers = []
        points = []
        b = Board(grid, blocks, lasers, points)
        sol = solve_bruteforce(b)
        self.assertIsNotNone(sol)  # empty-target case is trivially solved


if __name__ == "__main__":
    unittest.main()
