*This project has been created as part of the 42 curriculum by OlegGeroldi*

## Description

**A-Maze-ing** is an interactive maze generation and solving application that creates perfect and non-perfect mazes using advanced graph algorithms. The project demonstrates mastery of maze generation techniques, pathfinding algorithms, and interactive terminal-based visualization.

### Goal

The primary goal is to build a fully functional maze generator that:
- Generates mazes of configurable size using Kruskal's algorithm with union-find
- Incorporates the 42 school's iconic logo pattern into maze generation
- Finds optimal solutions using breadth-first search (BFS)
- Provides interactive visualization with multiple display themes
- Allows users to generate new mazes, toggle solution paths, and switch display themes

### Key Features

- **Two Maze Generation Modes**:
  - Perfect Mazes: Spanning trees with no cycles
  - Non-Perfect Mazes: Additional cycles with bounded open areas (max 3x3, 2x4, or 4x2)
- **42 Logo Pattern**: Integrated seamlessly into maze generation as blocked cells
- **Interactive Terminal UI**: Real-time maze display with menu controls
- **Solution Path Visualization**: Shows the shortest path from entry to exit
- **Multiple Rendering Themes**: Toggle between different visual styles
- **Configurable Parameters**: Customizable maze size, entry/exit points, and random seed
- **Persistent Output**: Mazes are automatically saved to a text file

---

## Instructions

### Prerequisites

- Python 3.10 or higher
- Standard Unix utilities (make)

### Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/maria-mld/a-maze-ing.git
   cd a-maze-ing
   ```

2. **Create virtual environment and install dependencies**:
   ```bash
   make venv
   make install
   ```

### Running the Application

1. **Run with default configuration**:
   ```bash
   make run
   ```

   This will use `config.txt` as the configuration file.

2. **Run with custom configuration**:
   ```bash
   python3 a_maze_ing.py /path/to/custom_config.txt
   ```

3. **Debug mode** (step through with pdb):
   ```bash
   make debug
   ```

### Configuration File Format

The `config.txt` file uses a simple key-value format:

```
WIDTH=20
HEIGHT=20
ENTRY=0,0
EXIT=19,19
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=5268135268
```

**Parameters**:
- `WIDTH`: Maze width in cells (integer, positive)
- `HEIGHT`: Maze height in cells (integer, positive)
- `ENTRY`: Starting position as `x,y` coordinates (must not be on the 42 pattern)
- `EXIT`: Goal position as `x,y` coordinates (must not be on the 42 pattern)
- `OUTPUT_FILE`: Path where the maze will be saved
- `PERFECT`: `True` for perfect mazes (spanning trees), `False` for non-perfect (with bounded cycles)
- `SEED`: Random seed for reproducible maze generation (integer, optional, defaults to 0)

**Validation Rules**:
- Entry and exit must be within maze bounds
- Entry and exit cannot be the same position
- Entry and exit cannot be on the 42 pattern cells
- Maze dimensions must be at least large enough to fit the 42 pattern (9x7 minimum)

### Interactive Controls

Once the application is running, use the following commands:

- **g** - Generate a new maze (increments seed)
- **s** - Show/hide the solution path
- **t** - Switch to the next display theme
- **q** - Quit the application

### Maintenance Commands

- **make clean**: Remove cache, build artifacts, and test files
- **make fclean**: Remove virtual environment and all generated files
- **make lint**: Run flake8 and mypy type checking
- **make build**: Build the distributable package
- **make package**: Create a Python wheel package

---

## Resources

### Maze Generation References

1. **Kruskal's Algorithm**: https://en.wikipedia.org/wiki/Kruskal%27s_algorithm
   - Classic minimum spanning tree algorithm adapted for maze generation
   
2. **Depth-First Search (DFS)**: https://en.wikipedia.org/wiki/Depth-first_search
   - Alternative maze generation approach
   
3. **Union-Find Data Structure**: https://en.wikipedia.org/wiki/Disjoint-set_data_structure
   - Efficient implementation for Kruskal's algorithm with path compression
   
4. **Breadth-First Search (BFS)**: https://en.wikipedia.org/wiki/Breadth-first_search
   - Used for finding shortest paths through mazes

5. **Maze Generation Algorithms**: http://www.astrolog.org/labyrnth/algrithm.htm
   - Comprehensive overview of various maze algorithms

### AI Usage

**Claude 3 Sonnet** was used for:
- **Architecture guidance**: Designing modular class structure for `MazeGenerator`, `MazeRenderer`, `PathFinder`, and `MazeWriter`
- **Code review and optimization**: Refactoring the union-find implementation and open area detection algorithm
- **Documentation**: Writing comprehensive docstrings and inline comments
- **Testing guidance**: Suggestions for edge case handling and parameter validation
- **Type hints**: Adding comprehensive type annotations throughout the codebase
- **Algorithm refinement**: Optimizing the non-perfect maze generation to bound open areas

---

## Configuration File Structure

### Complete Format

The configuration system uses a plain text key-value format with the following characteristics:

| Aspect | Details |
|--------|---------|
| **Format** | `KEY=VALUE` pairs, one per line |
| **Whitespace** | Automatically trimmed from keys and values |
| **Comments** | Lines starting with `#` are ignored |
| **Case** | Keys are converted to uppercase |
| **Parsing** | Handled by `MazeGenerator/parser.py` |
| **Mandatory Keys** | WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE |
| **Optional Keys** | PERFECT (defaults to True), SEED (defaults to 0) |

### Example Configurations

**Small maze for quick testing**:
```
WIDTH=10
HEIGHT=10
ENTRY=0,0
EXIT=9,9
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

**Large perfect maze**:
```
WIDTH=50
HEIGHT=50
ENTRY=1,1
EXIT=48,48
OUTPUT_FILE=large_maze.txt
PERFECT=True
SEED=12345
```

**Non-perfect maze with bounded open areas**:
```
WIDTH=30
HEIGHT=30
ENTRY=5,5
EXIT=24,24
OUTPUT_FILE=complex_maze.txt
PERFECT=False
SEED=999
```

---

## Maze Generation Algorithm

### Algorithm Choice: Kruskal's Algorithm with Union-Find

We implemented **Kruskal's Algorithm** combined with the **Union-Find (Disjoint-Set Union)** data structure for maze generation.

### Why Kruskal's Algorithm?

1. **Generates perfect mazes**: Guarantees a spanning tree with exactly one path between any two cells
2. **Efficient**: O(n log n) time complexity with randomized edge selection and union-find with path compression
3. **Deterministic seeding**: Produces reproducible mazes with fixed random seeds
4. **Conceptually elegant**: Works by progressively joining disconnected cells using a random process
5. **Naturally handles obstacles**: Easy to incorporate the 42 logo pattern as pre-blocked cells
6. **Extensible**: Simple to enhance with additional constraints (like bounded open areas)

### How It Works

**Perfect Maze Generation**:
1. **Initialize**: Create a grid where all cells are fully walled (value 15 = all walls closed)
2. **Identify blocked cells**: Mark cells that form the 42 logo pattern as permanently blocked
3. **Generate edges**: List all potential internal walls between adjacent unblocked cells
4. **Randomize and process**:
   - Shuffle the edge list using the seeded random generator
   - For each edge, check if its two cells are in different connected components (using union-find)
   - If they are different components, remove the wall between them and union the components
   - If they're already connected, skip the edge (to prevent cycles in perfect mazes)
5. **Result**: A perfect maze where every cell is reachable and there's exactly one path between any two cells

**Non-Perfect Maze Generation**:
1. Start with a perfect maze
2. Collect all walls that could be opened without violating cardinality constraints
3. For each candidate wall, temporarily open it and check if it creates a forbidden open area (3x3, 2x4, or 4x2)
4. If valid, permanently open the wall; otherwise, skip it
5. Stop when enough walls have been opened (bounded by maze width)

### Implementation Details

- **Wall encoding**: Each cell stores walls as a 4-bit integer:
  - Bit 1 (value 1): Top wall
  - Bit 2 (value 2): Right wall
  - Bit 3 (value 4): Bottom wall
  - Bit 4 (value 8): Left wall
- **Union-Find with path compression**: Optimizes component lookups with recursive path compression for nearly O(1) average performance
- **Open area detection**: Efficiently checks for forbidden rectangular regions to maintain playability
- **Non-perfect variant**: Adds random extra walls while maintaining bounded open areas to create more interesting mazes

---

## Reusable Code Components

### 1. **MazeGenerator Module** (Standalone library)

The `MazeGenerator` package is designed as a reusable Python library that can be integrated into other projects.

**How to reuse**:

```python
from MazeGenerator.maze_generator import PerfectMazeGen, NonPerfectMazeGen
from MazeGenerator.path_finder import PathFinder
from MazeGenerator.maze_renderer import MazeRenderer

# Create a generator
gen = PerfectMazeGen()
grid = gen.generate(width=20, height=20, seed=12345)

# Solve the maze
solution = PathFinder.solve(grid, (0, 0), (19, 19))

# Render it
renderer = MazeRenderer()
renderer.render(grid, (0, 0), solution, (19, 19))
```

**Available classes**:
- `PerfectMazeGen`: Generates spanning-tree mazes using Kruskal's algorithm
- `NonPerfectMazeGen`: Generates mazes with cycles and bounded open areas
- `PathFinder`: Static methods for BFS pathfinding
- `MazeRenderer`: Terminal visualization with multiple themes
- `MazeWriter`: Maze output to text files
- `Parser`: Configuration file parser

### 2. **MazeStrategy Pattern** (Design pattern)

The code implements the **Strategy Pattern** for maze generation:

```python
class MazeStrategy(ABC):
    @abstractmethod
    def generate(self, width: int, height: int, seed: int) -> List[List[int]]:
        """Generate a maze grid."""
        pass
```

This allows easy addition of new generation algorithms (DFS, Prims, Backtracking, etc.) without modifying existing code.

### 3. **Modular Components**

Each component is independent and can be used separately:

- **`parser.py`**: Configuration file parsing (reusable for any app needing config files)
- **`maze_renderer.py`**: Terminal rendering with theme system (applicable to any grid-based visualization)
- **`path_finder.py`**: BFS pathfinding (works for any grid-based pathfinding problem)
- **`maze_writer.py`**: Output formatting (adaptable for different maze formats)
- **`maze_generator.py`**: Maze generation strategies (extensible for new algorithms)

---

## Team and Project Management

### Team Members

**Solo Project**: Developed by **OlegGeroldi**

**Roles**:
- Full-stack development (architecture, implementation, testing)
- Requirements analysis and project planning
- Code optimization and refactoring
- Documentation and testing

### Planning and Evolution

#### Initial Planning

The project was approached with clear phases:

1. **Phase 1**: Core maze generation using Kruskal's algorithm
2. **Phase 2**: Pathfinding and solution visualization
3. **Phase 3**: Terminal rendering with themes
4. **Phase 4**: Configuration system and interactive UI
5. **Phase 5**: Non-perfect maze generation with open area constraints

#### Evolution and Changes

- **Initial design**: Started with a monolithic approach but refactored into modular components
- **Pattern integration**: Added the 42 logo pattern as a distinctive feature
- **Interactive UI**: Extended beyond static generation to include real-time user interaction
- **Theme system**: Implemented multiple rendering themes for better user experience
- **Type safety**: Added comprehensive type hints and mypy checking
- **Open area constraints**: Refined non-perfect maze generation to bound rectangular open areas

#### What Worked Well

✅ **Modular architecture**: Clear separation of concerns made testing and debugging easier  
✅ **Kruskal's algorithm**: Efficient and conceptually clean implementation  
✅ **Union-find optimization**: Path compression made the algorithm very fast  
✅ **Configuration system**: Flexible and easy to use for different maze parameters  
✅ **Interactive controls**: Real-time theme switching and maze regeneration  
✅ **Open area detection**: Sophisticated algorithm to ensure playable non-perfect mazes  
✅ **Type hints throughout**: Comprehensive type annotations prevented many bugs early  

#### What Could Be Improved

🔄 **Performance optimization**: Very large mazes (1000x1000+) could benefit from further optimizations  
🔄 **Advanced themes**: Could add more sophisticated rendering styles and ASCII art variants  
🔄 **Algorithm variants**: Could implement DFS, Prims, Backtracking for comparison  
🔄 **Web UI**: Terminal interface is functional but a web-based UI would be more accessible  
🔄 **Solver visualization**: Could animate the solution path being found in real-time  
🔄 **Performance metrics**: Could display generation and solving time statistics  
🔄 **Statistics mode**: Could generate statistics about maze properties (path length, branching factor, etc.)  

### Development Tools and Techniques

| Tool/Technique | Purpose |
|---|---|
| **Python 3.10+** | Primary programming language with modern features and type hints |
| **Type hints** | Static type checking with mypy for code reliability |
| **Makefile** | Build automation and convenient command shortcuts |
| **Virtual environment** | Isolated Python dependencies for reproducibility |
| **flake8** | Code style enforcement and linting |
| **mypy** | Static type analysis and bug prevention |
| **Git/GitHub** | Version control and collaboration |
| **Union-Find DS** | Efficient disjoint-set operations in Kruskal's algorithm |
| **Path compression** | Nearly O(1) amortized lookups in union-find |
| **BFS Algorithm** | Shortest-path finding for maze solutions |
| **Strategy Pattern** | Extensible maze generation algorithms |
| **Abstract Base Classes** | Enforces interface contracts for maze generators |

---

## Advanced Features

### Multiple Maze Generation Algorithms

The project supports two distinct generation modes:

1. **Perfect Mazes** (`PERFECT=True`)
   - Generates spanning trees with no cycles
   - Exactly one path between any two cells
   - Uses pure Kruskal's algorithm with union-find
   - Guaranteed solvability in O(width * height) cells

2. **Non-Perfect Mazes** (`PERFECT=False`)
   - Starts with a perfect maze
   - Adds random extra walls while respecting size constraints
   - Creates additional paths and loops for challenge
   - Prevents large empty areas (max 3x3, 2x4, or 4x2 cells)
   - Maintains playability and visual interest

### Open Area Constraint System

The non-perfect maze generator includes a sophisticated open area detection algorithm:
- Prevents creation of rectangular open areas larger than 3x3 cells
- Checks for 2x4 and 4x2 orientations as well
- Tests all positions where a wall change could occur
- Ensures mazes remain challenging and visually balanced

### Theme System

The `MazeRenderer` includes a theme system that allows users to switch between different visual styles:

- Multiple ASCII character sets for rendering walls and paths
- Color support for terminals (when available)
- Real-time theme switching during gameplay
- Easy to extend with new themes in `maze_renderer.py`

### Robust Configuration Parsing

The `Parser` class handles:
- Flexible whitespace handling (automatic trimming)
- Comment support (lines starting with `#`)
- Default values for optional parameters (PERFECT, SEED)
- Comprehensive error messages for invalid configurations
- Coordinate parsing in `x,y` format
- Case-insensitive key matching

### Comprehensive Parameter Validation

The `MazeEngine` validates all parameters before generation:
- Maze dimensions must be positive integers
- Entry and exit must be within bounds
- Entry and exit cannot be the same position
- Entry and exit cannot be on the 42 pattern cells
- Prevents invalid configurations early with clear error messages

---

## Quick Start Examples

### Generate a 20x20 maze and solve it
```bash
make run
# Use default config.txt, interact with menu
```

### Create a custom 30x30 perfect maze
```bash
cat > my_config.txt << EOF
WIDTH=30
HEIGHT=30
ENTRY=1,1
EXIT=28,28
OUTPUT_FILE=my_maze.txt
PERFECT=True
SEED=42
EOF

python3 a_maze_ing.py my_config.txt
```

### Generate a non-perfect maze with bounded open areas
```bash
cat > complex_maze.txt << EOF
WIDTH=40
HEIGHT=40
ENTRY=2,2
EXIT=37,37
OUTPUT_FILE=complex.txt
PERFECT=False
SEED=54321
EOF

python3 a_maze_ing.py complex_maze.txt
```

### Generate multiple mazes for testing
```bash
for i in {1..10}; do
  echo "Generating maze $i..."
  python3 a_maze_ing.py config.txt
done
```

---

## License

This project is part of the 42 School curriculum and is provided for educational purposes.

---

## Contributing

This is a curriculum project. Contributions and modifications are welcome for learning purposes.

---

## Contact

**Author**: OlegGeroldi  
**Repository**: https://github.com/maria-mld/a-maze-ing
