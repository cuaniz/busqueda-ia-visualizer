"""Local search algorithms for the 8 queens problem."""

from __future__ import annotations

import math
import random
from typing import Iterable

from search_visualizer.models import SearchStep

Board = tuple[int, ...]


def conflicts(board: Board) -> int:
    total = 0
    n = len(board)
    for r1 in range(n):
        for r2 in range(r1 + 1, n):
            c1, c2 = board[r1], board[r2]
            if c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                total += 1
    return total


def neighbors(board: Board) -> Iterable[Board]:
    n = len(board)
    for row in range(n):
        for col in range(n):
            if col != board[row]:
                candidate = list(board)
                candidate[row] = col
                yield tuple(candidate)


def random_board(seed: int | None = None, n: int = 8) -> Board:
    rng = random.Random(seed)
    return tuple(rng.randrange(n) for _ in range(n))


def hill_climbing(start: Board, max_steps: int = 200) -> list[SearchStep]:
    current = start
    history = [current]
    steps = [SearchStep("Inicio", "Hill Climbing parte de una configuración completa y busca vecinos con menos conflictos.", current, path=history.copy(), metadata={"conflictos": conflicts(current), "longitud_camino": len(history)})]

    for iteration in range(1, max_steps + 1):
        current_conflicts = conflicts(current)
        if current_conflicts == 0:
            steps.append(SearchStep("Solución encontrada", "No hay reinas atacándose entre sí.", current, path=history.copy(), metadata={"iteración": iteration, "conflictos": 0, "longitud_camino": len(history)}))
            return steps

        best_neighbor = min(neighbors(current), key=conflicts)
        best_conflicts = conflicts(best_neighbor)

        if best_conflicts >= current_conflicts:
            steps.append(SearchStep("Óptimo local", "Ningún vecino mejora la configuración actual; el algoritmo queda atrapado.", current, path=history.copy(), metadata={"iteración": iteration, "conflictos": current_conflicts, "mejor_vecino": best_conflicts, "longitud_camino": len(history)}))
            return steps

        current = best_neighbor
        history.append(current)
        steps.append(SearchStep("Mejor vecino", "Se mueve una reina para reducir la cantidad de conflictos.", current, path=history.copy(), metadata={"iteración": iteration, "conflictos": best_conflicts, "longitud_camino": len(history)}))

    steps.append(SearchStep("Límite alcanzado", "Se alcanzó el límite de iteraciones.", current, path=history.copy(), metadata={"conflictos": conflicts(current), "longitud_camino": len(history)}))
    return steps


def simulated_annealing(start: Board, seed: int | None = None, max_steps: int = 500, initial_temp: float = 10.0, cooling: float = 0.97) -> list[SearchStep]:
    rng = random.Random(seed)
    current = start
    history = [current]
    temperature = initial_temp
    steps = [SearchStep("Inicio", "Simulated Annealing acepta a veces movimientos peores para escapar de óptimos locales.", current, path=history.copy(), metadata={"conflictos": conflicts(current), "temperatura": temperature, "longitud_camino": len(history)})]

    for iteration in range(1, max_steps + 1):
        current_conflicts = conflicts(current)
        if current_conflicts == 0:
            steps.append(SearchStep("Solución encontrada", "La configuración no tiene conflictos.", current, path=history.copy(), metadata={"iteración": iteration, "conflictos": 0, "temperatura": temperature, "longitud_camino": len(history)}))
            return steps

        candidate = rng.choice(list(neighbors(current)))
        candidate_conflicts = conflicts(candidate)
        delta = current_conflicts - candidate_conflicts
        accepted = delta > 0
        probability = 1.0 if accepted else math.exp(delta / max(temperature, 0.0001))

        if not accepted and rng.random() < probability:
            accepted = True
        if accepted:
            current = candidate
            history.append(current)

        temperature *= cooling
        if iteration % 5 == 0 or accepted or candidate_conflicts == 0:
            steps.append(SearchStep("Evaluar vecino", "Se evalúa un vecino; puede aceptarse aunque sea peor según la temperatura.", current, path=history.copy(), metadata={"iteración": iteration, "conflictos": conflicts(current), "conflictos_candidato": candidate_conflicts, "aceptado": accepted, "temperatura": round(temperature, 4), "probabilidad": round(probability, 4), "longitud_camino": len(history)}))

        if temperature < 0.001:
            break

    steps.append(SearchStep("Fin", "Terminó el enfriamiento o se alcanzó el límite de iteraciones.", current, path=history.copy(), metadata={"conflictos": conflicts(current), "temperatura": round(temperature, 4), "longitud_camino": len(history)}))
    return steps
