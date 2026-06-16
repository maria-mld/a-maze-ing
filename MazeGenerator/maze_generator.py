from abc import ABC, abstractmethod
from typing import List, Set, Tuple
import random

Coordinate = Tuple[int, int]


class MazeStrategy(ABC):
    @abstractmethod
    def generate(self, width: int, height: int, seed: int) -> List[List[int]]:
        """Return a grid with walls encoded as bit masks."""
        pass


class PerfectMazeGen(MazeStrategy):
    PATTERN_42: Tuple[str, ...] = (
        "# # ###",
        "# #   #",
        "### ###",
        "  # #  ",
        "  # ###",
    )

    def generate(self, width: int, height: int, seed: int) -> List[List[int]]:
        random.seed(seed)
        # 15 = 1|2|4|8 (all walls are closed)
        grid = [[15 for _ in range(width)] for _ in range(height)]
        blocked = self.get_pattern_cells(width, height)

        # List all possible inner walls (edges)
        edges: List[Tuple[Coordinate, Coordinate, str]] = []
        for y in range(height):
            for x in range(width):
                if (x, y) in blocked:
                    continue
                if x < width - 1 and (x + 1, y) not in blocked:
                    edges.append(((x, y), (x + 1, y), 'E'))  # Right wall
                if y < height - 1 and (x, y + 1) not in blocked:
                    edges.append(((x, y), (x, y + 1), 'S'))  # Bottom wall

        random.shuffle(edges)
        parent = {
            (x, y): (x, y)
            for x in range(width)
            for y in range(height)
            if (x, y) not in blocked
        }

        def find(i: Coordinate) -> Coordinate:
            if parent[i] == i:
                return i
            parent[i] = find(parent[i])
            return parent[i]

        for (u, v, direction) in edges:
            root1, root2 = find(u), find(v)
            if root1 != root2:
                parent[root1] = root2
                self._remove_wall(grid, u, v, direction)

        return grid

    @classmethod
    def get_pattern_cells(cls, width: int, height: int,
                          warn: bool = True) -> Set[Coordinate]:
        """Return centered cells that form a closed-cell 42 pattern."""
        pattern_height = len(cls.PATTERN_42)
        pattern_width = len(cls.PATTERN_42[0])
        if width < pattern_width + 2 or height < pattern_height + 2:
            if warn:
                print("Error: maze is too small to contain the 42 pattern; "
                      "pattern omitted.")
            return set()

        left = (width - pattern_width) // 2
        top = (height - pattern_height) // 2
        cells: Set[Coordinate] = set()
        for row_index, row in enumerate(cls.PATTERN_42):
            for column_index, char in enumerate(row):
                if char == "#":
                    cells.add((left + column_index, top + row_index))
        return cells

    def _remove_wall(self, grid: List[List[int]],
                     u: Coordinate,
                     v: Coordinate,
                     direction: str) -> None:
        ux, uy = u
        vx, vy = v
        if direction == 'E':
            grid[uy][ux] &= ~2  # Remove the current cell's right wall
            grid[vy][vx] &= ~8  # Remove the neighbor's left wall
        elif direction == 'S':
            grid[uy][ux] &= ~4  # Remove the current cell's bottom wall
            grid[vy][vx] &= ~1  # Remove the neighbor's top wall


class NonPerfectMazeGen(PerfectMazeGen):
    def generate(self, width: int, height: int, seed: int) -> List[List[int]]:
        grid = super().generate(width, height, seed)
        blocked = self.get_pattern_cells(width, height, warn=False)

        extra_edges: List[Tuple[Coordinate, Coordinate, str]] = []
        for y in range(height):
            for x in range(width):
                if (x, y) in blocked:
                    continue
                if (x < width - 1 and (x + 1, y) not in blocked
                        and (grid[y][x] & 2)):
                    extra_edges.append(((x, y), (x + 1, y), 'E'))
                if (y < height - 1 and (x, y + 1) not in blocked
                        and (grid[y][x] & 4)):
                    extra_edges.append(((x, y), (x, y + 1), 'S'))

        random.shuffle(extra_edges)
        for u, v, direction in extra_edges[:width]:
            self._remove_wall(grid, u, v, direction)

        return grid
