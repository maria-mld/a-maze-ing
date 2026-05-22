from abc import ABC, abstractmethod
from typing import List, Tuple
import random

class MazeStrategy(ABC):
    @abstractmethod
    def generate(self, width: int, height: int, seed: int) -> List[List[int]]:
        """Возвращает сетку с закодированными стенами."""
        pass

class PerfectMazeGen(MazeStrategy):
    def generate(self, width: int, height: int, seed: int) -> List[List[int]]:
        random.seed(seed)
        # 15 = 1|2|4|8 (все стены закрыты)
        grid = [[15 for _ in range(width)] for _ in range(height)]
        
        # Список всех возможных стен (ребер)
        edges = []
        for y in range(height):
            for x in range(width):
                if x < width - 1: edges.append(((x, y), (x + 1, y), 'E')) # Стена справа
                if y < height - 1: edges.append(((x, y), (x, y + 1), 'S')) # Стена снизу
        
        random.shuffle(edges)
        parent = {(x, y): (x, y) for x in range(width) for y in range(height)}

        def find(i):
            if parent[i] == i: return i
            parent[i] = find(parent[i])
            return parent[i]

        for (u, v, direction) in edges:
            root1, root2 = find(u), find(v)
            if root1 != root2:
                parent[root1] = root2
                self._remove_wall(grid, u, v, direction)
        
        return grid

    def _remove_wall(self, grid: List[List[int]], u: Tuple[int, int], v: Tuple[int, int], direction: str):
        ux, uy = u
        vx, vy = v
        if direction == 'E':
            grid[uy][ux] &= ~2  # Убираем стену справа у текущей
            grid[vy][vx] &= ~8  # Убираем стену слева у соседки
        elif direction == 'S':
            grid[uy][ux] &= ~4  # Убираем стену снизу у текущей
            grid[vy][vx] &= ~1  # Убираем стену сверху у соседки

class NonPerfectMazeGen(PerfectMazeGen):
    def generate(self, width: int, height: int, seed: int) -> List[List[int]]:
        grid = super().generate(width, height, seed)
        # Добавляем случайные "дыры" в стены, чтобы создать циклы
        for _ in range(width):
            x, y = random.randint(0, width-1), random.randint(0, height-1)
            grid[y][x] = 0 # "Пробиваем" случайную ячейку
        return grid
    
