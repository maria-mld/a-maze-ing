from typing import Tuple, List
from MazeGenerator.maze_generator import PerfectMazeGen, NonPerfectMazeGen
from MazeGenerator.path_finder import PathFinder
from MazeGenerator.maze_writer import MazeWriter
from MazeGenerator.maze_renderer import MazeRenderer


class MazeEngine:
    """Orchestrates maze generation, solving, and rendering."""

    def __init__(self, width: int, height: int, entry: Tuple[int, int],
                 exit_coords: Tuple[int, int], output_file: str,
                 perfect: bool, seed: int) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_coords = exit_coords
        self.output_file = output_file
        self.seed = seed
        self.solution = ""
        self._validate_parameters()

        # Choose the generation strategy based on the perfect flag
        if perfect:
            self.generator = PerfectMazeGen()
        else:
            self.generator = NonPerfectMazeGen()

        self.grid: List[List[int]] = []
        self.renderer = MazeRenderer()
        self.writer = MazeWriter(output_file)

    def _validate_parameters(self) -> None:
        """Validate size and coordinates before generation starts."""
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Maze width and height must be positive")
        if not self._is_inside(self.entry):
            raise ValueError("Entry coordinates are outside the maze")
        if not self._is_inside(self.exit_coords):
            raise ValueError("Exit coordinates are outside the maze")
        if self.entry == self.exit_coords:
            raise ValueError("Entry and exit coordinates must be different")

        pattern_cells = PerfectMazeGen.get_pattern_cells(self.width,
                                                         self.height,
                                                         warn=False)
        if self.entry in pattern_cells:
            raise ValueError("Entry coordinates cannot be on the 42 pattern")
        if self.exit_coords in pattern_cells:
            raise ValueError("Exit coordinates cannot be on the 42 pattern")

    def _is_inside(self, point: Tuple[int, int]) -> bool:
        """Return whether the coordinate is inside the maze."""
        x, y = point
        return 0 <= x < self.width and 0 <= y < self.height

    def generate(self) -> None:
        """Executes the selected generation strategy."""
        self.grid = self.generator.generate(self.width, self.height, self.seed)

    def solve(self) -> None:
        """Finds the shortest path using the pathfinder module."""
        self.solution = PathFinder.solve(self.grid,
                                         self.entry, self.exit_coords)

    def save(self) -> None:
        """Saves the maze using the writer."""
        self.writer.write(self.grid, self.entry,
                          self.exit_coords, self.solution)

    def show(self, with_path: bool) -> None:
        """Visualizes the maze via the new renderer."""
        self.renderer.render(
            grid=self.grid,
            start=self.entry,
            path_str=self.solution if with_path else "",
            end_coords=self.exit_coords,
            show_path=with_path
        )
