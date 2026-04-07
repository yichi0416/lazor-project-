import os

def read_bff(file_path):
    """Read a .bff file and return contents."""

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # remove comments and empty lines
    clean_lines = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            clean_lines.append(line)

    return clean_lines


def parse_grid(lines):
    """Extract the grid from lines."""

    grid = []
    inside_grid = False

    for line in lines:
        if line == "GRID START":
            inside_grid = True
            continue

        if line == "GRID STOP":
            inside_grid = False
            continue

        if inside_grid:
            row = line.split()
            new_row = []

            for cell in row:
                new_row.append(cell)

            grid.append(new_row)

    return grid


def parse_available_blocks(lines):
    """Extract available block"""

    available_blocks = {"A": 0, "B": 0, "C": 0}

    for line in lines:
        parts = line.split()
        if len(parts) == 2 and parts[0] in available_blocks:
            available_blocks[parts[0]] = int(parts[1])

    return available_blocks


def parse_lasers(lines):
    """Extract lazor starting points and directions."""

    lasers = []

    for line in lines:
        parts = line.split()
        if parts[0] == "L":
            x = int(parts[1])
            y = int(parts[2])
            vx = int(parts[3])
            vy = int(parts[4])
            lasers.append((x, y, vx, vy))

    return lasers


def parse_points(lines):
    """Extract target points."""

    points = []

    for line in lines:
        parts = line.split()
        if parts[0] == "P":
            x = int(parts[1])
            y = int(parts[2])
            points.append((x, y))

    return points


def parse_bff(file_path):
    """Read and parse one .bff file."""

    lines = read_bff(file_path)

    puzzle = {
        "grid": parse_grid(lines),
        "available_blocks": parse_available_blocks(lines),
        "lasers": parse_lasers(lines),
        "points": parse_points(lines)
    }

    return puzzle


if __name__ == "__main__":
    folder = "bff_files"

    for filename in os.listdir(folder):
        if filename.endswith(".bff"):
            path = os.path.join(folder, filename)

            print(f"\n===== Reading {filename} =====")

            puzzle = parse_bff(path)

            print("Grid:")
            for row in puzzle["grid"]:
                print(row)

            print("Available Blocks:", puzzle["available_blocks"])
            print("Lasers:", puzzle["lasers"])
            print("Points:", puzzle["points"])
