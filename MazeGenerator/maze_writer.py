from typing import List, Tuple


class MazeWriter:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def write(self, grid: List[List[int]], entry: Tuple[int, int],
              exit_coords: Tuple[int, int], path: str) -> None:
        """Save the maze to a file."""
        with open(self.filename, "w") as f:
            for row in grid:
                f.write("".join(f"{cell:X}" for cell in row) + "\n")
            f.write(f"\n{entry[0]},"
                    f"{entry[1]}\n{exit_coords[0]},{exit_coords[1]}\n{path}\n")
