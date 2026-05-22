import sys
from MazeGenerator.parser import Parser
from MazeGenerator.maze_engine import MazeEngine

def print_menu() -> None:
    print("\n--- Maze Generator Menu ---")
    print("g - Generate new maze")
    print("s - Show/Hide solution path")
    print("t - Next theme")
    print("q - Quit")
    print("---------------------------")

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <path_to_config>")
        return

    config_path = sys.argv[1]
    try:
        # Инициализация
        parser = Parser(config_path)
        engine = MazeEngine(*parser.get_args())
        
        # Первая генерация
        engine.generate()
        engine.solve()
        engine.save()

        show_path = True
        
        # Игровой цикл
        while True:
            # 1. Очистка (один раз в начале)
            print("\033[H\033[J", end="")
            
            # 2. Вывод состояния
            print(f"Current Theme: {engine.renderer.get_current_theme_name()}")
            print(f"Output File: {engine.output_file} (Autosaved)")

            # 3. Отрисовка лабиринта
            engine.show(with_path=show_path)
            print_menu()

            # 4. ЖДЕМ ввода (программа встанет здесь)
            choice = input("Select action: ").lower().strip()

            # 5. Обработка команд
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
    main()

