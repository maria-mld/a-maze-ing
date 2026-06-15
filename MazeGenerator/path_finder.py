from typing import List, Tuple
from collections import deque


class PathFinder:
    @staticmethod
    def solve(grid: List[List[int]],
              start: Tuple[int, int],
              end: Tuple[int, int]) -> str:
        queue = deque([(start, "")])
        visited = {start}

        while queue:
            (x, y), path = queue.popleft()

            if (x, y) == end:
                return path

            cell = grid[y][x]
            # Check neighbors (bits: 1=N, 2=E, 4=S, 8=W)
            # If a bit is not set, that side is open.

            # North (N)
            if not (cell & 1) and (x, y - 1) not in visited:
                visited.add((x, y - 1))
                queue.append(((x, y - 1), path + "N"))
            # East (E)
            if not (cell & 2) and (x + 1, y) not in visited:
                visited.add((x + 1, y))
                queue.append(((x + 1, y), path + "E"))
            # South (S)
            if not (cell & 4) and (x, y + 1) not in visited:
                visited.add((x, y + 1))
                queue.append(((x, y + 1), path + "S"))
            # West (W)
            if not (cell & 8) and (x - 1, y) not in visited:
                visited.add((x - 1, y))
                queue.append(((x - 1, y), path + "W"))

        return ""  # No path found
