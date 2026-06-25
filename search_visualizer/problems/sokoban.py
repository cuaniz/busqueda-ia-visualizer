

from __future__ import annotations

from dataclasses import dataclass

Position = tuple[int, int]
SokobanState = tuple[Position, frozenset[Position]]


@dataclass(frozen=True)
class Sokoban:
    grid: tuple[str, ...] = (
        "######",
        "#.P..#",
        "#..B.#",
        "#.B.G#",
        "#.G..#",
        "######",
    )

    def __post_init__(self) -> None:
        walls: set[Position] = set()
        goals: set[Position] = set()
        boxes: set[Position] = set()
        player = (0, 0)
        for r, row in enumerate(self.grid):
            for c, value in enumerate(row):
                if value == "#":
                    walls.add((r, c))
                elif value == "G":
                    goals.add((r, c))
                elif value == "B":
                    boxes.add((r, c))
                elif value == "P":
                    player = (r, c)
        if len(boxes) != 2:
            raise ValueError(f"Sokoban requiere exactamente 2 cajas, se encontraron {len(boxes)}")
        if len(goals) != 2:
            raise ValueError(f"Sokoban requiere exactamente 2 objetivos, se encontraron {len(goals)}")
        if len(goals) != len(set(goals)):
            raise ValueError("Los objetivos de Sokoban deben estar en posiciones distintas")
        if boxes == goals:
            raise ValueError("Las cajas de Sokoban no deben iniciar sobre los objetivos")
        object.__setattr__(self, "walls", frozenset(walls))
        object.__setattr__(self, "goals", frozenset(goals))
        object.__setattr__(self, "start", (player, frozenset(boxes)))
        object.__setattr__(self, "height", len(self.grid))
        object.__setattr__(self, "width", len(self.grid[0]))

    def is_goal(self, state: SokobanState) -> bool:
        _player, boxes = state
        return boxes == self.goals

    def is_free(self, pos: Position, boxes: frozenset[Position]) -> bool:
        return pos not in self.walls and pos not in boxes

    def successors(self, state: SokobanState) -> list[tuple[str, SokobanState, float]]:
        player, boxes = state
        moves = [
            ("Arriba", (-1, 0)),
            ("Abajo", (1, 0)),
            ("Izquierda", (0, -1)),
            ("Derecha", (0, 1)),
        ]
        result = []
        for action, (dr, dc) in moves:
            next_player = (player[0] + dr, player[1] + dc)
            if next_player in self.walls:
                continue
            if next_player in boxes:
                pushed_box = (next_player[0] + dr, next_player[1] + dc)
                if not self.is_free(pushed_box, boxes):
                    continue
                new_boxes = set(boxes)
                new_boxes.remove(next_player)
                new_boxes.add(pushed_box)
                result.append((f"Empujar {action}", (next_player, frozenset(new_boxes)), 1.0))
            elif next_player not in boxes:
                result.append((action, (next_player, boxes), 1.0))
        return result

    def heuristic(self, state: SokobanState) -> float:
        _player, boxes = state
        total = 0
        for box in boxes:
            total += min(abs(box[0] - goal[0]) + abs(box[1] - goal[1]) for goal in self.goals)
        return float(total)
