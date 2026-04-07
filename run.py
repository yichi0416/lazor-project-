#!/usr/bin/env python3
# Lazor Unified Solver - Batch Compatible Version (Final)
# EN.540.635 Software Carpentry – 2026

from __future__ import annotations
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import List, Tuple, Dict, Optional, Set
import argparse
import sys
import time

Cell = str
Point = Tuple[int, int]


# ----------------------------------------------------------------------
# Basic data classes
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Ray:
    """Represents a single laser ray."""
    x: int
    y: int
    vx: int
    vy: int


@dataclass
class Board:
    """Represents Lazor grid board, laser positions, and targets."""
    grid: List[List[Cell]]
    lasers: List[Ray]
    targets: List[Point]

    @property
    def H(self) -> int:
        return len(self.grid)

    @property
    def W(self) -> int:
        return len(self.grid[0]) if self.grid else 0

    def cell_at(self, r: int, c: int) -> Optional[Cell]:
        if 0 <= r < self.H and 0 <= c < self.W:
            return self.grid[r][c]
        return None


# ----------------------------------------------------------------------
# Parsing .bff files
# ----------------------------------------------------------------------
def _tok_int(s: str) -> int:
    return int(s.replace("=", ""))


def parse_bff(path: Path) -> Tuple[Board, Dict[str, int], List[Tuple[int, int]]]:
    """Read .bff file and return Board, inventory, and open slots."""
    lines: List[str] = []
    for raw in path.read_text().splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        lines.append(s)

    grid: List[List[Cell]] = []
    lasers: List[Ray] = []
    targets: List[Point] = []
    inv = {"A": 0, "B": 0, "C": 0}

    i = 0
    while i < len(lines):
        tok = lines[i]
        up = tok.upper()
        if up == "GRID START":
            i += 1
            buf: List[List[Cell]] = []
            while i < len(lines) and lines[i].upper() != "GRID STOP":
                row = list(lines[i].replace(" ", ""))
                if any(ch not in {"o", "x", "A", "B", "C"} for ch in row):
                    raise ValueError(f"Invalid GRID line: {lines[i]}")
                buf.append(row)
                i += 1
            grid = buf
        elif tok[0] in {"A", "B", "C"} and len(tok.split()) == 2:
            kind, num = tok.split()
            inv[kind] = _tok_int(num)
        elif tok.startswith("L"):
            _, sx, sy, vx, vy = tok.split()
            lasers.append(Ray(_tok_int(sx), _tok_int(sy), _tok_int(vx), _tok_int(vy)))
        elif tok.startswith("P"):
            _, px, py = tok.split()
            targets.append((_tok_int(px), _tok_int(py)))
        i += 1

    if not grid:
        raise ValueError("Missing GRID data in file.")

    open_slots = [(r, c)
                  for r in range(len(grid))
                  for c in range(len(grid[0]))
                  if grid[r][c] == "o"]

    return Board(grid=grid, lasers=lasers, targets=targets), inv, open_slots


# ----------------------------------------------------------------------
# Simulation Physics
# ----------------------------------------------------------------------
def trace_all_rays(board: Board, step_cap: int = 10000) -> Set[Point]:
    """Compute all laser paths and record hit targets."""
    hit: Set[Point] = set()
    rays: List[Ray] = list(board.lasers)
    seen: Set[Tuple[int, int, int, int]] = set()

    xmax, ymax = board.W * 2, board.H * 2

    while rays:
        ray = rays.pop()
        x, y, vx, vy = ray.x, ray.y, ray.vx, ray.vy
        steps = 0

        while 0 <= x <= xmax and 0 <= y <= ymax:
            if steps > step_cap:
                break
            state = (x, y, vx, vy)
            if state in seen:
                break
            seen.add(state)

            nx, ny = x + vx, y + vy
            if nx < 0 or nx > xmax or ny < 0 or ny > ymax:
                break

            blocked = False
            mx, my = (x + nx) // 2, (y + ny) // 2
            crossed_vertical = (nx % 2 == 0)
            crossed_horizontal = (ny % 2 == 0)

            orig_vx, orig_vy = vx, vy
            if crossed_vertical and crossed_horizontal:
                col = max(0, min(nx // 2 - (1 if vx < 0 else 0), board.W - 1))
                row = max(0, min(ny // 2 - (1 if vy < 0 else 0), board.H - 1))
                cell = board.cell_at(row, col)
                if cell == "A":
                    vx, vy = -vx, -vy
                elif cell == "B":
                    blocked = True
                elif cell == "C":
                    rays.append(Ray(nx, ny, -orig_vx, -orig_vy))
            elif crossed_vertical:
                col = max(0, min(nx // 2 - (1 if vx < 0 else 0), board.W - 1))
                row = max(0, min(my // 2, board.H - 1))
                cell = board.cell_at(row, col)
                if cell == "A":
                    vx = -vx
                elif cell == "B":
                    blocked = True
                elif cell == "C":
                    rays.append(Ray(nx, ny, -orig_vx, orig_vy))
            elif crossed_horizontal:
                row = max(0, min(ny // 2 - (1 if vy < 0 else 0), board.H - 1))
                col = max(0, min(mx // 2, board.W - 1))
                cell = board.cell_at(row, col)
                if cell == "A":
                    vy = -vy
                elif cell == "B":
                    blocked = True
                elif cell == "C":
                    rays.append(Ray(nx, ny, orig_vx, -orig_vy))

            if blocked:
                break
            x, y = nx, ny
            steps += 1
            if (x, y) in board.targets:
                hit.add((x, y))
    return hit


# ----------------------------------------------------------------------
# Search algorithm
# ----------------------------------------------------------------------
def grid_to_string(grid: List[List[Cell]]) -> str:
    return "\n".join("".join(row) for row in grid)


def place_and_solve(base: Board, inv: Dict[str, int], open_slots: List[Tuple[int, int]], diagnose: bool = False) -> Optional[List[List[Cell]]]:
    """Try placing blocks to hit all targets."""
    nA, nB, nC = inv["A"], inv["B"], inv["C"]
    total_blocks = nA + nB + nC
    if total_blocks > len(open_slots):
        print("Inventory exceeds number of open slots.")
        return None

    targets = set(base.targets)
    grid0 = [row[:] for row in base.grid]
    best_hit, best_layout = 0, None
    count, total_combos = 0, 1

    total_combos *= max(1, len(open_slots) ** total_blocks)

    start_time = time.time()
    for posC in combinations(open_slots, nC) if nC <= len(open_slots) else [()]:
        remA = [p for p in open_slots if p not in posC]
        for posA in combinations(remA, nA) if nA <= len(remA) else [()]:
            remB = [p for p in remA if p not in posA]
            for posB in combinations(remB, nB) if nB <= len(remB) else [()]:
                count += 1
                g = [row[:] for row in grid0]
                for r, c in posA: g[r][c] = "A"
                for r, c in posB: g[r][c] = "B"
                for r, c in posC: g[r][c] = "C"

                got = trace_all_rays(Board(grid=g, lasers=base.lasers, targets=base.targets))
                if len(got) > best_hit:
                    best_hit = len(got)
                    best_layout = [row[:] for row in g]
                    print(f"  • New best: {best_hit}/{len(targets)} targets")

                if got >= targets:
                    duration = time.time() - start_time
                    print(f"\n✅ Found solution after {count} combinations ({duration:.2f}s)!")
                    return g

    if diagnose:
        print(f"\nDiagnosis: best hit {best_hit}/{len(targets)} targets.")
        if best_layout:
            print(grid_to_string(best_layout))
    return best_layout if best_hit > 0 else None


# ----------------------------------------------------------------------
# IO helpers
# ----------------------------------------------------------------------
def write_solution(path: Path, grid: List[List[Cell]]):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(grid_to_string(grid), encoding="utf-8")


# ----------------------------------------------------------------------
# CLI entrypoint
# ----------------------------------------------------------------------
def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Lazor Unified Solver - Final Version")
    parser.add_argument("-i", "--input", help=".bff file path (optional with --all)")
    parser.add_argument("-o", "--output", help="Output file path (ignored with --all)")
    parser.add_argument("--diagnose", action="store_true", help="Enable diagnosis mode")
    parser.add_argument("--all", action="store_true", help="Solve every .bff in data/")
    args = parser.parse_args(argv)

    # Mode: solve all files
    if args.all:
        data_dir = Path("data")
        if not data_dir.exists():
            print("❌ data directory not found.")
            return 2
        files = list(data_dir.glob("*.bff"))
        if not files:
            print("No .bff files found in data/")
            return 0

        print(f"\n📦 Found {len(files)} .bff files in data/")
        summary = []
        for f in files:
            t0 = time.time()
            print(f"\n🧩 Solving {f.name} ...")
            board, inv, slots = parse_bff(f)
            sol = place_and_solve(board, inv, slots, diagnose=args.diagnose)
            t1 = time.time() - t0
            if sol:
                outp = f.with_name(f.stem + "_solution.txt")
                write_solution(outp, sol)
                print(f"✅ {f.name} solved → {outp.name} ({t1:.2f}s)")
                summary.append((f.name, True, t1))
            else:
                print(f"✗ No solution found for {f.name} ({t1:.2f}s)")
                summary.append((f.name, False, t1))

        print("\n──────────────── Summary ────────────────")
        for name, ok, secs in summary:
            status = "✓" if ok else "✗"
            print(f"{status} {name:20s}  {secs:6.2f}s")
        print("─────────────────────────────────────────")
        return 0

    # Mode: single file
    if not args.input or not args.output:
        print("Error: -i and -o must be provided (unless --all used).")
        return 2

    path_in = Path(args.input)
    if not path_in.exists():
        print(f"Input .bff not found: {path_in}")
        return 2
    board, inv, slots = parse_bff(path_in)
    print(f"\n🧩 Processing {path_in.name}")
    print(f"- Grid: {board.H}x{board.W}")
    print(f"- Inventory: A={inv['A']} B={inv['B']} C={inv['C']}")
    print(f"- Open slots: {len(slots)} | Targets: {len(board.targets)}")

    sol = place_and_solve(board, inv, slots, diagnose=args.diagnose)
    if not sol:
        print("\n✗ No solution found.")
        return 1

    path_out = Path(args.output)
    write_solution(path_out, sol)
    print(f"\n✅ Solution saved → {path_out}")
    print(grid_to_string(sol))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())