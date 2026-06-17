"""Output writer for generated maze files."""

from typing import List, Tuple


class MazeWriter:
    """Write maze grids and solutions to the required text format."""

    def __init__(self, filename: str) -> None:
        """Initialize a writer for an output file.

        Args:
            filename: Destination file path.
        """
        self.filename = filename

    def write(self, grid: List[List[int]], entry: Tuple[int, int],
              exit_coords: Tuple[int, int], path: str) -> None:
        """Save the maze grid, coordinates, and solution path to a file.

        Args:
            grid: Maze grid encoded as wall bit masks.
            entry: Entry cell coordinate.
            exit_coords: Exit cell coordinate.
            path: Solution path represented with ``N``, ``E``, ``S``, and
            ``W`` characters.
        """
        with open(self.filename, "w") as f:
            for row in grid:
                f.write("".join(f"{cell:X}" for cell in row) + "\n")
            f.write(f"\n{entry[0]},"
                    f"{entry[1]}\n{exit_coords[0]},{exit_coords[1]}\n{path}\n")
