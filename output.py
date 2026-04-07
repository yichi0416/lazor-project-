from .board import Board


def write_solution_text(board, path):
    """Write solved board information to a text file."""

    with open(path, "w") as f:
        f.write("Solution placements (r c kind fixed/placed):\n")

        for position, block in sorted(board.cells.items()):
            r, c = position

            if block is not None:
                if block.fixed:
                    status = "fixed"
                else:
                    status = "placed"

                f.write(f"{r} {c} {block.kind} {status}\n")

        f.write("\nLasers:\n")
        for laser in board.lasers:
            lx = laser[0]
            ly = laser[1]
            vx = laser[2]
            vy = laser[3]
            f.write(f"L {lx} {ly} {vx} {vy}\n")

        f.write("\nPoints:\n")
        for point in board.points:
            px = point[0]
            py = point[1]
            f.write(f"P {px} {py}\n")
