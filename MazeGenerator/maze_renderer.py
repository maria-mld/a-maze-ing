"""Terminal renderer for generated mazes."""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class Theme:
    """Store ANSI colors used to draw a maze theme."""

    name: str
    wall: str
    path: str


class MazeRenderer:
    """Draws the generated maze in the terminal."""

    CELL_WIDTH = 2

    WALL = "█"
    PATH = "█"
    EMPTY = " "
    CLOSED_CELL = "░"

    RESET = "\033[0m"
    DIM = "\033[90m"
    START = "\033[92m"
    EXIT = "\033[96m"

    THEMES: List[Theme] = [
        Theme("Moonlight", "\033[37m", "\033[96m"),
        Theme("Rose Garden", "\033[95m", "\033[92m"),
        Theme("Amber Cave", "\033[33m", "\033[91m"),
        Theme("Ice Lake", "\033[36m", "\033[94m"),
        Theme("Lime Wire", "\033[92m", "\033[93m"),
        Theme("Soft Shadow", "\033[90m", "\033[97m"),
    ]

    OPENINGS: Dict[int, Tuple[int, int]] = {
        1: (0, -1),   # north
        2: (1, 0),    # east
        4: (0, 1),    # south
        8: (-1, 0),   # west
    }

    PATH_STEPS: Dict[str, Tuple[int, int]] = {
        "N": (0, -1),
        "E": (1, 0),
        "S": (0, 1),
        "W": (-1, 0),
    }

    def __init__(self) -> None:
        """Initialize the renderer with the first available theme."""
        self.theme_index = 0

    def next_theme(self) -> str:
        """Switch to the next color theme.

        Returns:
            The name of the newly selected theme.
        """
        self.theme_index = (self.theme_index + 1) % len(self.THEMES)
        return self.get_current_theme_name()

    def get_current_theme_name(self) -> str:
        """Return the name of the active color theme."""
        return self.THEMES[self.theme_index].name

    def render(
        self,
        grid: List[List[int]],
        start: Tuple[int, int],
        path_str: str = "",
        end_coords: Optional[Tuple[int, int]] = None,
        show_path: bool = False,
    ) -> None:
        """Draw a maze in the terminal.

        Args:
            grid: Maze grid encoded as wall bit masks.
            start: Entry coordinate.
            path_str: Solution path represented with direction letters.
            end_coords: Exit coordinate. If omitted, it is inferred by walking
            ``path_str`` from ``start``.
            show_path: Whether to draw the solution path.
        """
        if not grid or not grid[0]:
            return

        canvas = self._make_canvas(len(grid[0]), len(grid))
        self._draw_passages(canvas, grid)

        if show_path and path_str:
            self._draw_path(canvas, start, path_str)

        self._paint(canvas, self._cell_to_canvas(start), self.WALL, self.START)

        if end_coords is not None:
            end_point = self._cell_to_canvas(end_coords)
        else:
            end_point = self._walk_path(start, path_str)
        self._paint(canvas, end_point, self.WALL, self.EXIT)

        self._print(canvas)

    def _make_canvas(self, width: int, height: int) -> List[List[str]]:
        """Create a wall-filled terminal canvas for a maze size.

        Args:
            width: Maze width in cells.
            height: Maze height in cells.

        Returns:
            A two-dimensional character canvas initialized with wall symbols.
        """
        theme = self.THEMES[self.theme_index]
        wall = self._color(self.WALL, theme.wall)
        canvas_width = (width * 2 + 1) * self.CELL_WIDTH
        canvas_height = height * 2 + 1
        return [
            [wall for _ in range(canvas_width)]
            for _ in range(canvas_height)
        ]

    def _draw_passages(
        self,
        canvas: List[List[str]],
        grid: List[List[int]],
    ) -> None:
        """Carve visible passages into the terminal canvas.

        Args:
            canvas: Character canvas to mutate.
            grid: Maze grid encoded as wall bit masks.
        """
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                point = self._cell_to_canvas((x, y))

                if cell == 15:
                    self._paint(canvas, point, self.CLOSED_CELL, self.DIM)
                else:
                    self._paint(canvas, point, self.EMPTY)

                for wall, step in self.OPENINGS.items():
                    if not (cell & wall):
                        self._paint(
                            canvas,
                            self._offset(point, step),
                            self.EMPTY,
                        )

    def _draw_path(
        self,
        canvas: List[List[str]],
        start: Tuple[int, int],
        path: str,
    ) -> None:
        """Draw a solution path on the terminal canvas.

        Args:
            canvas: Character canvas to mutate.
            start: Coordinate where the path begins.
            path: Direction string using ``N``, ``E``, ``S``, and ``W``.
        """
        theme = self.THEMES[self.theme_index]
        point = self._cell_to_canvas(start)
        self._paint(canvas, point, self.PATH, theme.path)

        for direction in path:
            step = self.PATH_STEPS[direction]
            self._paint(
                canvas,
                self._offset(point, step),
                self.PATH,
                theme.path,
            )
            point = self._offset(point, (step[0] * 2, step[1] * 2))
            self._paint(canvas, point, self.PATH, theme.path)

    def _walk_path(
        self,
        start: Tuple[int, int],
        path: str,
    ) -> Tuple[int, int]:
        """Return the final canvas point reached by a path.

        Args:
            start: Maze coordinate where the path begins.
            path: Direction string to follow.

        Returns:
            Canvas coordinate reached after walking the path.
        """
        point = self._cell_to_canvas(start)
        for direction in path:
            step = self.PATH_STEPS[direction]
            point = self._offset(point, (step[0] * 2, step[1] * 2))
        return point

    def _cell_to_canvas(self, cell: Tuple[int, int]) -> Tuple[int, int]:
        """Convert a maze cell coordinate to a canvas coordinate."""
        x, y = cell
        return x * 2 + 1, y * 2 + 1

    def _offset(
        self,
        point: Tuple[int, int],
        step: Tuple[int, int],
    ) -> Tuple[int, int]:
        """Return a point moved by a step vector."""
        return point[0] + step[0], point[1] + step[1]

    def _paint(
        self,
        canvas: List[List[str]],
        point: Tuple[int, int],
        char: str,
        color: str = "",
    ) -> None:
        """Paint a character on the canvas with optional ANSI color.

        Args:
            canvas: Character canvas to mutate.
            point: Canvas coordinate to paint.
            char: Character to place on the canvas.
            color: Optional ANSI color escape sequence.
        """
        x, y = point
        value = self._color(char, color) if color else char
        for stretch in range(self.CELL_WIDTH):
            canvas[y][x * self.CELL_WIDTH + stretch] = value

    def _color(self, char: str, color: str) -> str:
        """Wrap a character in an ANSI color escape sequence."""
        return f"{color}{char}{self.RESET}"

    def _print(self, canvas: List[List[str]]) -> None:
        """Print a character canvas to the terminal."""
        for row in canvas:
            print("".join(row))
