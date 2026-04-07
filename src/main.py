import sys
import os
from .parser import parse_bff
from .board import Board
from .solver import solve_bruteforce
from .output import write_solution_text


def main(bff_path, out_dir="outputs"):
    """Run solver on one bff file."""

    # check file exists
    if not os.path.exists(bff_path):
        print("File not found:", bff_path)
        return

    # read and parse file
    data = parse_bff(bff_path)

    grid = data["grid"]
    available_blocks = data["available_blocks"]
    lasers = data["lasers"]
    points = data["points"]

    # create board object
    board = Board(grid, available_blocks, lasers, points)

    # make output folder if needed
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    print("Parsed board:", board.rows, "x", board.cols)
    print("Allowed positions:", len(board.allowed))

    # run solver
    solution = solve_bruteforce(board)

    # write result
    if solution is None:
        print("No solution found.")
    else:
        filename = os.path.splitext(os.path.basename(bff_path))[0]
        out_path = os.path.join(out_dir, filename + "_solution.txt")
        write_solution_text(solution, out_path)
        print("Solution written to", out_path)


if __name__ == "__main__":
    # get input file
    if len(sys.argv) > 1:
        bff = sys.argv[1]
    else:
        bff = "data/test.bff"

    main(bff)
