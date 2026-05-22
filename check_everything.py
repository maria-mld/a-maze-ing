from MazeGenerator.parser import Parser
from MazeGenerator.maze_engine import MazeEngine

def test_flow():
    print("--- Starting Full System Check ---")
    try:
        # 1. Проверяем парсер (убедитесь, что config.txt лежит в той же папке)
        parser = Parser("config.txt")
        args = parser.get_args()
        print("✅ Parser: OK (Конфиг прочитан)")

        # 2. Проверяем движок и генератор
        engine = MazeEngine(*args)
        engine.generate()
        print(f"✅ Generation: OK (Лабиринт {args[0]}x{args[1]} создан)")

        # 3. Проверяем решатель
        engine.solve()
        print("✅ Solver: OK (Путь найден)")

        # 4. Проверяем запись
        engine.save()
        print(f"✅ Save: OK (Файл {args[4]} успешно записан)")

    except Exception as e:
        print(f"❌ Error during test: {e}")
        # Если возникла ошибка, она подскажет, где именно проблема
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_flow()

