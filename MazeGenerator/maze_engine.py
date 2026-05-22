from typing import Tuple
from .maze_generator import PerfectMazeGen, NonPerfectMazeGen
from .path_finder import PathFinder
from .maze_writer import MazeWriter
from .maze_renderer import MazeRenderer

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
        
        # Выбираем стратегию в зависимости от флага perfect 
        if perfect:
            self.generator = PerfectMazeGen()
        else:
            self.generator = NonPerfectMazeGen()
            
        self.grid = []
        self.renderer = MazeRenderer()
        self.writer = MazeWriter(output_file)

    def generate(self) -> None:
        """Executes the selected generation strategy."""
        self.grid = self.generator.generate(self.width, self.height, self.seed)

    def solve(self) -> None:
        """Finds the shortest path using the pathfinder module."""
        self.solution = PathFinder.solve(self.grid, self.entry, self.exit_coords)

    def save(self) -> None:
        """Saves the maze using the writer."""
        self.writer.write(self.grid, self.entry, self.exit_coords, self.solution)

    def show(self, with_path: bool) -> None:
        """Visualizes the maze via the new renderer."""
        # Передаем все необходимые аргументы
        self.renderer.render(
            grid=self.grid,
            start=self.entry,
            path_str=self.solution if with_path else "",
            end_coords=self.exit_coords,
            show_path=with_path
        )
