import os

def read_bff(file_path):
    """Read a .bff file and return its contents."""

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
    """Extract the grid from cleaned lines."""

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
            grid.append(row)

    return grid


if __name__ == "__main__":
    folder = "bff_files"

    for filename in os.listdir(folder):
        if filename.endswith(".bff"):
            path = os.path.join(folder, filename)

            print(f"\n===== Reading {filename} =====")

            data = read_bff(path)
            grid = parse_grid(data)

            print("Grid:")
            for row in grid:
                print(row)
