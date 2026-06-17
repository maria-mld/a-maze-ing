"""Command-line entry point for the A-Maze-ing project."""

import sys
from MazeGenerator.parser import Parser
from MazeGenerator.maze_engine import MazeEngine


def print_menu() -> None:
    """Print the interactive terminal menu."""
    print("\n--- Maze Generator Menu ---")
    print("g - Generate new maze")
    print("s - Show/Hide solution path")
    print("t - Next theme")
    print("q - Quit")
    print("---------------------------")


def main() -> None:
    """Run the maze generator from a configuration file.

    The program expects exactly one command-line argument: the path to a
    configuration file. It loads the configuration, generates and solves the
    maze, saves the result, then starts an interactive terminal loop.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <path_to_config>")
        return

    config_path = sys.argv[1]
    try:
        parser = Parser(config_path)
        engine = MazeEngine(*parser.get_args())

        engine.generate()
        engine.solve()
        engine.save()

        show_path = True

        while True:
            print("\033[H\033[J", end="")

            print(f"Current Theme: {engine.renderer.get_current_theme_name()}")
            print(f"Output File: {engine.output_file} (Autosaved)")

            engine.show(with_path=show_path)
            print_menu()

            choice = input("Select action: ").lower().strip()

            if choice == "g":
                engine.seed += 1
                engine.generate()
                engine.solve()
                engine.save()
            elif choice == "s":
                show_path = not show_path
            elif choice == "t":
                engine.renderer.next_theme()
            elif choice == "q":
                print("Goodbye!")
                break

    except Exception as e:
        print(f"Critical Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n Interrupted")
