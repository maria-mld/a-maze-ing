"""Maze generation strategies used by the A-Maze-ing project."""

from abc import ABC, abstractmethod
from typing import List, Set, Tuple
import random

Coordinate = Tuple[int, int]


class MazeStrategy(ABC):
    """Define the common interface for maze generation strategies."""

    @abstractmethod
    def generate(self, width: int, height: int, seed: int) -> List[List[int]]:
        """Generate a maze grid.

        Args:
            width: Number of cells on the horizontal axis.
            height: Number of cells on the vertical axis.
            seed: Random seed used to make generation reproducible.

        Returns:
            A two-dimensional grid of wall bit masks.
        """
        pass


class PerfectMazeGen(MazeStrategy):
    """Generate a perfect maze with a centered closed-cell 42 pattern."""

    PATTERN_42: Tuple[str, ...] = (
        "# # ###",
        "# #   #",
        "### ###",
        "  # #  ",
        "  # ###",
    )

    def generate(self, width: int, height: int, seed: int) -> List[List[int]]:
        """Generate a perfect maze using randomized Kruskal's algorithm.

        Args:
            width: Number of cells on the horizontal axis.
            height: Number of cells on the vertical axis.
            seed: Random seed used to shuffle candidate walls.

        Returns:
            A maze grid where each cell is encoded as a wall bit mask.
        """
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
            """Return the representative coordinate for a disjoint set."""
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
        """Return centered cells that form a closed-cell 42 pattern.

        Args:
            width: Maze width in cells.
            height: Maze height in cells.
            warn: Whether to print a message when the maze is too small.

        Returns:
            A set of coordinates that must stay fully closed.
        """
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
        """Open the shared wall between two neighboring cells.

        Args:
            grid: Maze grid to mutate.
            u: First cell coordinate.
            v: Second cell coordinate.
            direction: Direction from ``u`` to ``v``.
        """
        ux, uy = u
        vx, vy = v
        if direction == 'E':
            grid[uy][ux] &= ~2  # Remove the current cell's right wall
            grid[vy][vx] &= ~8  # Remove the neighbor's left wall
        elif direction == 'S':
            grid[uy][ux] &= ~4  # Remove the current cell's bottom wall
            grid[vy][vx] &= ~1  # Remove the neighbor's top wall


class NonPerfectMazeGen(PerfectMazeGen):
    """Generate a non-perfect maze while limiting open area size."""

    def generate(self, width: int, height: int, seed: int) -> List[List[int]]:
        """Generate a maze with extra loops and bounded open areas.

        The method starts from a perfect maze, then opens additional walls when
        doing so does not create an open area larger than 2x3 or 3x2 cells.

        Args:
            width: Number of cells on the horizontal axis.
            height: Number of cells on the vertical axis.
            seed: Random seed inherited from the perfect maze generation.

        Returns:
            A non-perfect maze grid encoded as wall bit masks.
        """
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
        opened_count = 0
        for u, v, direction in extra_edges:
            if opened_count >= width:
                break
            if self._can_remove_wall(grid, u, v, direction):
                self._remove_wall(grid, u, v, direction)
                opened_count += 1

        return grid

    def _can_remove_wall(self, grid: List[List[int]],
                         u: Coordinate,
                         v: Coordinate,
                         direction: str) -> bool:
        """Return whether removing a wall keeps open areas at most 2x3.

        Args:
            grid: Maze grid to test.
            u: First cell coordinate.
            v: Second cell coordinate.
            direction: Direction from ``u`` to ``v``.

        Returns:
            True if the wall can be removed without creating a forbidden open
            area, otherwise False.
        """
        self._remove_wall(grid, u, v, direction)
        creates_large_area = self._has_large_open_area(grid, u, v)
        self._add_wall(grid, u, v, direction)
        return not creates_large_area

    def _add_wall(self, grid: List[List[int]],
                  u: Coordinate,
                  v: Coordinate,
                  direction: str) -> None:
        """Close the shared wall between two neighboring cells.

        Args:
            grid: Maze grid to mutate.
            u: First cell coordinate.
            v: Second cell coordinate.
            direction: Direction from ``u`` to ``v``.
        """
        ux, uy = u
        vx, vy = v
        if direction == 'E':
            grid[uy][ux] |= 2
            grid[vy][vx] |= 8
        elif direction == 'S':
            grid[uy][ux] |= 4
            grid[vy][vx] |= 1

    def _has_large_open_area(self, grid: List[List[int]],
                             u: Coordinate,
                             v: Coordinate) -> bool:
        """Check whether changed cells belong to a forbidden open area.

        Args:
            grid: Maze grid to inspect.
            u: First cell affected by a tentative wall change.
            v: Second cell affected by a tentative wall change.

        Returns:
            True if a fully open 3x3, 2x4, or 4x2 area exists around the
            changed cells, otherwise False.
        """
        height = len(grid)
        width = len(grid[0]) if height else 0
        forbidden_sizes = [(3, 3), (2, 4), (4, 2)]
        changed_cells = [u, v]

        for area_width, area_height in forbidden_sizes:
            for cell_x, cell_y in changed_cells:
                left_start = cell_x - area_width + 1
                top_start = cell_y - area_height + 1
                for left in range(left_start, cell_x + 1):
                    for top in range(top_start, cell_y + 1):
                        if (0 <= left and left + area_width <= width
                                and 0 <= top
                                and top + area_height <= height):
                            if self._is_open_area(
                                grid,
                                left,
                                top,
                                area_width,
                                area_height,
                            ):
                                return True
        return False

    def _is_open_area(self, grid: List[List[int]], left: int, top: int,
                      width: int, height: int) -> bool:
        """Return whether a rectangular area is fully open internally.

        Args:
            grid: Maze grid to inspect.
            left: Leftmost x-coordinate of the rectangle.
            top: Topmost y-coordinate of the rectangle.
            width: Rectangle width in cells.
            height: Rectangle height in cells.

        Returns:
            True when all cells exist, are not fully closed, and have no
            internal walls between them.
        """
        for y in range(top, top + height):
            for x in range(left, left + width):
                if grid[y][x] == 15:
                    return False
                if x < left + width - 1 and (grid[y][x] & 2):
                    return False
                if y < top + height - 1 and (grid[y][x] & 4):
                    return False
        return True
