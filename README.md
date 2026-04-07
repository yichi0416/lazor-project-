# lazor-project-
# Lazor Solver Project

## Overview
This project implements a solver for Lazor puzzles using Python.  
The program reads a `.bff` file, constructs the puzzle board, places blocks using a search algorithm, and simulates laser paths to determine whether all target points are hit.

---

## Features
- Parse `.bff` puzzle files
- Represent board and block placements
- Backtracking / combination-based solver
- Laser ray tracing simulation
- Output solution to file

---

## Project Structure
src/
├── main.py          # Entry point
├── parser.py        # Reads and parses .bff files
├── board.py         # Board and block representation
├── ray.py           # Ray class
├── tracer.py        # Laser simulation
├── solver.py        # Solver logic
├── solver_utils.py  # Solution checking
├── output.py        # Write results to file
---

## How It Works

1. **Parsing**
   - The `.bff` file is read and converted into:
     - Grid
     - Available blocks (A, B, C)
     - Laser sources
     - Target points

2. **Board Setup**
   - A `Board` object stores:
     - Allowed block positions
     - Current placements
     - Laser and target information

3. **Solving**
   - The solver generates combinations of block placements
   - For each configuration:
     - Blocks are placed on the board
     - Laser paths are simulated

4. **Ray Tracing**
   - Rays move in small steps
   - Interactions:
     - `A`: reflect
     - `B`: absorb (stop)
     - `C`: split into two rays

5. **Validation**
   - A solution is valid if all target points are hit

---

## How to Run

From the project root:

```bash
python -m src.main data/test.bff

To run another specific test:
python -m src.main data/"example test name".bff
