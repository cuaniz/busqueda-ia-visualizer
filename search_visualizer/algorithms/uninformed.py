"""Uninformed search algorithms for graph-like problems."""

from __future__ import annotations

from collections import deque
from heapq import heappop, heappush
from itertools import count
from typing import Any, Callable, Iterable

from search_visualizer.models import SearchStep

SuccessorFn = Callable[[Any], Iterable[tuple[str, Any, float]]]
GoalFn = Callable[[Any], bool]


def reconstruct_path(parent: dict[Any, tuple[Any, str] | None], goal: Any) -> list[Any]:
    path = [goal]
    current = goal
    while parent[current] is not None:
        current = parent[current][0]  # type: ignore[index]
        path.append(current)
    path.reverse()
    return path


def breadth_first_search(start: Any, is_goal: GoalFn, successors: SuccessorFn, max_steps: int = 500) -> list[SearchStep]:
    frontier = deque([start])
    parent: dict[Any, tuple[Any, str] | None] = {start: None}
    visited: set[Any] = set()
    steps = [SearchStep("Inicio", "BFS usa una cola FIFO: expande primero los estados más cercanos.", start, list(frontier), visited.copy(), [start])]

    while frontier and len(steps) < max_steps:
        current = frontier.popleft()
        if current in visited:
            continue
        visited.add(current)
        current_path = reconstruct_path(parent, current)

        if is_goal(current):
            steps.append(SearchStep("Meta encontrada", "BFS encontró la solución de menor número de pasos.", current, list(frontier), visited.copy(), current_path))
            return steps

        for action, nxt, _cost in successors(current):
            if nxt not in visited and nxt not in parent:
                parent[nxt] = (current, action)
                frontier.append(nxt)

        steps.append(SearchStep("Expandir nodo", "Se extrae el primer estado de la cola y se agregan sucesores no visitados.", current, list(frontier), visited.copy(), current_path, metadata={"visitados": len(visited), "frontera": len(frontier), "longitud_camino": len(current_path)}))

    steps.append(SearchStep("Sin solución", "La frontera quedó vacía o se alcanzó el límite de pasos.", None, list(frontier), visited.copy()))
    return steps


def depth_first_search(start: Any, is_goal: GoalFn, successors: SuccessorFn, max_steps: int = 500) -> list[SearchStep]:
    frontier = [start]
    parent: dict[Any, tuple[Any, str] | None] = {start: None}
    visited: set[Any] = set()
    steps = [SearchStep("Inicio", "DFS usa una pila LIFO: profundiza por un camino antes de retroceder.", start, frontier.copy(), visited.copy(), [start])]

    while frontier and len(steps) < max_steps:
        current = frontier.pop()
        if current in visited:
            continue
        visited.add(current)
        current_path = reconstruct_path(parent, current)

        if is_goal(current):
            steps.append(SearchStep("Meta encontrada", "DFS encontró una solución, pero no necesariamente la óptima.", current, frontier.copy(), visited.copy(), current_path))
            return steps

        generated = []
        for action, nxt, _cost in successors(current):
            if nxt not in visited and nxt not in parent:
                parent[nxt] = (current, action)
                generated.append(nxt)
        frontier.extend(reversed(generated))

        steps.append(SearchStep("Expandir nodo", "Se extrae el último estado de la pila y se continúa profundizando.", current, frontier.copy(), visited.copy(), current_path, metadata={"visitados": len(visited), "frontera": len(frontier), "longitud_camino": len(current_path)}))

    steps.append(SearchStep("Sin solución", "La frontera quedó vacía o se alcanzó el límite de pasos.", None, frontier.copy(), visited.copy()))
    return steps


def uniform_cost_search(start: Any, is_goal: GoalFn, successors: SuccessorFn, max_steps: int = 500) -> list[SearchStep]:
    tie = count()
    frontier: list[tuple[float, int, Any]] = []
    heappush(frontier, (0.0, next(tie), start))
    parent: dict[Any, tuple[Any, str] | None] = {start: None}
    best_cost: dict[Any, float] = {start: 0.0}
    visited: set[Any] = set()
    steps = [SearchStep("Inicio", "UCS prioriza el menor costo acumulado g(n).", start, [start], visited.copy(), [start], metadata={"g": 0.0})]

    while frontier and len(steps) < max_steps:
        cost, _tie, current = heappop(frontier)
        if current in visited:
            continue
        visited.add(current)
        current_path = reconstruct_path(parent, current)

        if is_goal(current):
            steps.append(SearchStep("Meta encontrada", "UCS encontró la solución de menor costo acumulado.", current, [item[2] for item in frontier], visited.copy(), current_path, {"g": cost, "longitud_camino": len(current_path)}))
            return steps

        for action, nxt, step_cost in successors(current):
            new_cost = cost + step_cost
            if nxt not in best_cost or new_cost < best_cost[nxt]:
                best_cost[nxt] = new_cost
                parent[nxt] = (current, action)
                heappush(frontier, (new_cost, next(tie), nxt))

        steps.append(SearchStep("Expandir nodo", "Se expande el estado con menor costo acumulado en la cola de prioridad.", current, [item[2] for item in frontier], visited.copy(), current_path, metadata={"g": cost, "visitados": len(visited), "frontera": len(frontier), "longitud_camino": len(current_path)}))

    steps.append(SearchStep("Sin solución", "La frontera quedó vacía o se alcanzó el límite de pasos.", None, [item[2] for item in frontier], visited.copy()))
    return steps
