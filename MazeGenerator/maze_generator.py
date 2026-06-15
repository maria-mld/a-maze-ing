from abc import ABC, abstractmethod
from typing import List, Tuple
import random


class MazeStrategy(ABC):
    @abstractmethod
    def generate(self, width: int, height: int, seed: int) -> List[List[int]]:
        """Return a grid with walls encoded as bit masks."""
        pass


class PerfectMazeGen(MazeStrategy):
    def generate(self, width: int, height: int, seed: int) -> List[List[int]]:
        random.seed(seed)
        # 15 = 1|2|4|8 (all walls are closed)
        grid = [[15 for _ in range(width)] for _ in range(height)]

        # List all possible inner walls (edges)
        edges = []
        for y in range(height):
            for x in range(width):
                if x < width - 1:
                    edges.append(((x, y), (x + 1, y), 'E'))  # Right wall
                if y < height - 1:
                    edges.append(((x, y), (x, y + 1), 'S'))  # Bottom wall

        random.shuffle(edges)
        parent = {(x, y): (x, y) for x in range(width) for y in range(height)}

        def find(i: Tuple[int, int]) -> Tuple[int, int]:
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

    def _remove_wall(self, grid: List[List[int]],
                     u: Tuple[int, int],
                     v: Tuple[int, int],
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
        # Add random openings to create loops
        for _ in range(width):
            x, y = random.randint(0, width-1), random.randint(0, height-1)
            grid[y][x] = 0  # Open a random cell
        return grid
