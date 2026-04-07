# lazor-project-
# Lazor Solver Project

Description
This repository contains:

run.py: command-line solver that reads puzzle files in BFF format, tries combinations of placements according to available inventory, and outputs solution grids.
data/: example puzzle files (.bff)
solution/: output solution files
tests/: test cases
Requirements

Python 3.7+
No external dependencies (uses only standard library modules)
Installation

Clone the repository: git clone <repo-url>
Enter the directory: cd <repo-dir>
Usage
Single puzzle:

run.py -i data/example.bff -o solution/example_solution.txt This parses the input, runs the solver, and writes the solution grid to the specified output file.
Solve all puzzles in data/:

run.py --all This will iterate over all .bff files in data/ and write a corresponding *_sol.txt file in the same folder.
Options

-i : input .bff file path
-o : output file path for the solution grid
--all : solve every .bff file found in the data directory
--debug : print debug information and best partial solution if no full solution found
Input format (BFF)

GRID START / GRID STOP: ASCII grid rows between these markers. Use characters for empty cells or pre-filled items.
LASERS: list of lasers with coordinates and direction (format same as in examples)
TARGETS: list of target coordinates
INVENTORY: counts for A, B, C pieces (e.g., A=2, B=1, C=0) (Replace with exact syntax from your example .bff files; add a short example.)
How the solver works (brief)

Reads board, laser definitions, targets and inventory.
Enumerates combinations of empty slots for placing A, B, and C devices according to inventory counts.
For each placement, simulates laser rays across the board using reflection, blocking, and C-piece behavior to collect hit targets.
Returns the first configuration that hits all targets; otherwise returns the best partial solution (if --debug is used prints best hit count).
Output

Plain-text grid: same dimensions as input grid, with A/B/C placed where solution puts them. Each row is a line in the output file.
Testing

Tests are in the tests/ directory. Run them with your preferred test runner or inspect the example test cases.
Contributing

Fork the repository, make a branch, open a PR. Add tests for new features and document changes in the README.
License

Add your license here (e.g., MIT). If you don’t want to include a license, state that all rights are reserved.
Contact

Add maintainer email or GitHub handle.
