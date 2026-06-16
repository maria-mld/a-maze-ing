from typing import List, Tuple
from collections import deque


class PathFinder:
    @staticmethod
    def solve(grid: List[List[int]],
              start: Tuple[int, int],
              end: Tuple[int, int]) -> str:
        height = len(grid)
        width = len(grid[0]) if height else 0

        def is_inside(x: int, y: int) -> bool:
            return 0 <= x < width and 0 <= y < height

        if not is_inside(*start) or not is_inside(*end):
            return ""

        queue = deque([(start, "")])
        visited = {start}

        def add_if_valid(next_x: int, next_y: int,
                         next_path: str) -> None:
            if not is_inside(next_x, next_y):
                return
            if (next_x, next_y) in visited:
                return
            visited.add((next_x, next_y))
            queue.append(((next_x, next_y), next_path))

        while queue:
            (x, y), path = queue.popleft()

            if (x, y) == end:
                return path

            cell = grid[y][x]
            # Check neighbors (bits: 1=N, 2=E, 4=S, 8=W)
            # If a bit is not set, that side is open.

            # North (N)
            if not (cell & 1):
                add_if_valid(x, y - 1, path + "N")
            # East (E)
            if not (cell & 2):
                add_if_valid(x + 1, y, path + "E")
            # South (S)
            if not (cell & 4):
                add_if_valid(x, y + 1, path + "S")
            # West (W)
            if not (cell & 8):
                add_if_valid(x - 1, y, path + "W")

        return ""  # No path found
