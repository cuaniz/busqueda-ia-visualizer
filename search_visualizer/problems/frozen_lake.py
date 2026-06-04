"""Frozen Lake deterministic grid problem."""

from __future__ import annotations

from dataclasses import dataclass

Position = tuple[int, int]


@dataclass(frozen=True)
class FrozenLake:
    grid: tuple[str, ...] = (
        "SFFF",
        "FHFH",
        "FFFH",
        "HFFG",
    )

    def __post_init__(self) -> None:
        object.__setattr__(self, "height", len(self.grid))
        object.__setattr__(self, "width", len(self.grid[0]))
        object.__setattr__(self, "start", self._find("S"))
        object.__setattr__(self, "goal", self._find("G"))

    def _find(self, target: str) -> Position:
        for r, row in enumerate(self.grid):
            for c, value in enumerate(row):
                if value == target:
                    return (r, c)
        raise ValueError(f"Missing {target}")

    def is_goal(self, state: Position) -> bool:
        return state == self.goal

    def successors(self, state: Position) -> list[tuple[str, Position, float]]:
        moves = [
            ("Arriba", (-1, 0)),
            ("Abajo", (1, 0)),
            ("Izquierda", (0, -1)),
            ("Derecha", (0, 1)),
        ]
        result = []
        for action, (dr, dc) in moves:
            nr, nc = state[0] + dr, state[1] + dc
            if 0 <= nr < self.height and 0 <= nc < self.width and self.grid[nr][nc] != "H":
                result.append((action, (nr, nc), 1.0))
        return result
