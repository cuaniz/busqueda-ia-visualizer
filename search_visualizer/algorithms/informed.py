"""Informed search algorithms for Sokoban and similar state spaces."""

from __future__ import annotations

from heapq import heappop, heappush
from itertools import count
from typing import Any, Callable, Iterable

from search_visualizer.algorithms.uninformed import reconstruct_path
from search_visualizer.models import SearchStep

SuccessorFn = Callable[[Any], Iterable[tuple[str, Any, float]]]
GoalFn = Callable[[Any], bool]
HeuristicFn = Callable[[Any], float]


def a_star_search(start: Any, is_goal: GoalFn, successors: SuccessorFn, heuristic: HeuristicFn, max_steps: int = 1500) -> list[SearchStep]:
    tie = count()
    frontier: list[tuple[float, int, Any]] = []
    heappush(frontier, (heuristic(start), next(tie), start))
    parent: dict[Any, tuple[Any, str] | None] = {start: None}
    g_score: dict[Any, float] = {start: 0.0}
    visited: set[Any] = set()
    steps = [SearchStep("Inicio", "A* usa f(n) = g(n) + h(n).", start, [start], visited.copy(), [start], metadata={"g": 0.0, "h": heuristic(start), "f": heuristic(start)})]

    while frontier and len(steps) < max_steps:
        _priority, _tie, current = heappop(frontier)
        if current in visited:
            continue
        visited.add(current)
        g = g_score[current]
        h = heuristic(current)
        current_path = reconstruct_path(parent, current)

        if is_goal(current):
            steps.append(SearchStep("Meta encontrada", "A* encontró una solución usando costo acumulado y heurística.", current, [item[2] for item in frontier], visited.copy(), current_path, {"g": g, "h": h, "f": g + h, "longitud_camino": len(current_path)}))
            return steps

        for action, nxt, cost in successors(current):
            tentative_g = g + cost
            if nxt not in g_score or tentative_g < g_score[nxt]:
                parent[nxt] = (current, action)
                g_score[nxt] = tentative_g
                heappush(frontier, (tentative_g + heuristic(nxt), next(tie), nxt))

        steps.append(SearchStep("Expandir nodo", "A* expande el estado con menor f(n).", current, [item[2] for item in frontier], visited.copy(), current_path, metadata={"g": g, "h": h, "f": g + h, "visitados": len(visited), "frontera": len(frontier), "longitud_camino": len(current_path)}))

    steps.append(SearchStep("Sin solución", "La frontera quedó vacía o se alcanzó el límite de pasos.", None, [item[2] for item in frontier], visited.copy()))
    return steps


def greedy_best_first_search(start: Any, is_goal: GoalFn, successors: SuccessorFn, heuristic: HeuristicFn, max_steps: int = 1500) -> list[SearchStep]:
    tie = count()
    frontier: list[tuple[float, int, Any]] = []
    heappush(frontier, (heuristic(start), next(tie), start))
    parent: dict[Any, tuple[Any, str] | None] = {start: None}
    visited: set[Any] = set()
    steps = [SearchStep("Inicio", "Greedy prioriza solo h(n): el estado que parece más cercano a la meta.", start, [start], visited.copy(), [start], metadata={"h": heuristic(start)})]

    while frontier and len(steps) < max_steps:
        _h, _tie, current = heappop(frontier)
        if current in visited:
            continue
        visited.add(current)
        h = heuristic(current)
        current_path = reconstruct_path(parent, current)

        if is_goal(current):
            steps.append(SearchStep("Meta encontrada", "Greedy encontró una solución, aunque no garantiza optimalidad.", current, [item[2] for item in frontier], visited.copy(), current_path, {"h": h, "longitud_camino": len(current_path)}))
            return steps

        for action, nxt, _cost in successors(current):
            if nxt not in visited and nxt not in parent:
                parent[nxt] = (current, action)
                heappush(frontier, (heuristic(nxt), next(tie), nxt))

        steps.append(SearchStep("Expandir nodo", "Greedy expande el estado con menor estimación heurística h(n).", current, [item[2] for item in frontier], visited.copy(), current_path, metadata={"h": h, "visitados": len(visited), "frontera": len(frontier), "longitud_camino": len(current_path)}))

    steps.append(SearchStep("Sin solución", "La frontera quedó vacía o se alcanzó el límite de pasos.", None, [item[2] for item in frontier], visited.copy()))
    return steps
