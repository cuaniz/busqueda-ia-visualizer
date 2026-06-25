

from __future__ import annotations

from collections import deque
from typing import Any, Callable, Iterable

from search_visualizer.models import SearchStep

SuccessorFn = Callable[[Any], Iterable[tuple[str, Any, float]]]
GoalFn = Callable[[Any], bool]
StateToIdFn = Callable[[Any], int]


def _make_metadata(
    visited: Iterable[Any],
    frontier: list[Any],
    current: Any | None,
    path_len: int,
    state_to_id: StateToIdFn | None = None,
    comentario: str = "",
) -> dict[str, Any]:
    visited_list = list(visited)
    if state_to_id is not None:
        return {
            "visitados": [state_to_id(s) for s in visited_list],
            "frontera": [state_to_id(s) for s in frontier],
            "nodo_actual": state_to_id(current) if current is not None else None,
            "longitud_camino": path_len,
            "comentario": comentario,
        }
    return {
        "visitados": len(visited_list),
        "frontera": len(frontier),
        "longitud_camino": path_len,
    }


def reconstruct_path(parent: dict[Any, tuple[Any, str] | None], goal: Any) -> list[Any]:
    path = [goal]
    current = goal
    while parent[current] is not None:
        current = parent[current][0] 
        path.append(current)
    path.reverse()
    return path


def breadth_first_search(
    start: Any,
    is_goal: GoalFn,
    successors: SuccessorFn,
    state_to_id: StateToIdFn | None = None,
    max_steps: int = 500,
) -> list[SearchStep]:
    frontier = deque([start])
    parent: dict[Any, tuple[Any, str] | None] = {start: None}
    visited: set[Any] = set()
    visited_order: list[Any] = []
    steps = [SearchStep("Inicio", "BFS usa una cola FIFO: expande primero los estados más cercanos.", start, list(frontier), visited.copy(), [start], metadata=_make_metadata(set(), list(frontier), start, 1, state_to_id))]

    while frontier and len(steps) < max_steps:
        current = frontier.popleft()
        if current in visited:
            continue
        visited.add(current)
        visited_order.append(current)
        current_path = reconstruct_path(parent, current)

        if is_goal(current):
            steps.append(SearchStep("Meta encontrada", "BFS encontró la solución de menor número de pasos.", current, list(frontier), visited.copy(), current_path, metadata=_make_metadata(visited_order, list(frontier), current, len(current_path), state_to_id)))
            return steps

        for action, nxt, _cost in successors(current):
            if nxt not in visited and nxt not in parent:
                parent[nxt] = (current, action)
                frontier.append(nxt)

        steps.append(SearchStep("Expandir nodo", "Se extrae el primer estado de la cola y se agregan sucesores no visitados.", current, list(frontier), visited.copy(), current_path, metadata=_make_metadata(visited_order, list(frontier), current, len(current_path), state_to_id)))

    steps.append(SearchStep("Sin solución", "La frontera quedó vacía o se alcanzó el límite de pasos.", None, list(frontier), visited.copy(), metadata=_make_metadata(visited_order, list(frontier), None, 0, state_to_id, "No se encontró solución; la frontera está vacía.")))
    return steps


def depth_first_search(
    start: Any,
    is_goal: GoalFn,
    successors: SuccessorFn,
    state_to_id: StateToIdFn | None = None,
    max_steps: int = 500,
) -> list[SearchStep]:

    frontier = [start]
    parent: dict[Any, tuple[Any, str] | None] = {start: None}
    visited: set[Any] = set()
    visited_order: list[Any] = []
    current_path: list[Any] = [start]
    steps = [SearchStep("Inicio", "DFS usa una pila LIFO: profundiza por un camino antes de retroceder.", start, frontier.copy(), visited.copy(), current_path.copy(), metadata=_make_metadata(set(), frontier.copy(), start, 1, state_to_id))]

    while frontier and len(steps) < max_steps:
        current = frontier.pop()
        if current in visited:
            continue
        visited.add(current)
        visited_order.append(current)
        current_path = reconstruct_path(parent, current)

        if is_goal(current):
            steps.append(SearchStep("Meta encontrada", "DFS encontró una solución, pero no necesariamente la óptima.", current, frontier.copy(), visited.copy(), current_path, metadata=_make_metadata(visited_order, frontier.copy(), current, len(current_path), state_to_id, "DFS alcanzó la meta por el camino actual de la pila.")))
            return steps

        generated: list[Any] = []
        for action, nxt, _cost in successors(current):
            if nxt not in visited and nxt not in parent:
                parent[nxt] = (current, action)
                generated.append(nxt)
        frontier.extend(reversed(generated))

        comentario = ""
        if not generated:

            comentario = "DFS no encontró sucesores no visitados; retrocede (backtrack) y prueba la siguiente rama de la pila."

        steps.append(SearchStep("Expandir nodo", "Se extrae el último estado de la pila y se continúa profundizando.", current, frontier.copy(), visited.copy(), current_path, metadata=_make_metadata(visited_order, frontier.copy(), current, len(current_path), state_to_id, comentario)))

    steps.append(SearchStep("Sin solución", "La frontera quedó vacía o se alcanzó el límite de pasos.", None, frontier.copy(), visited.copy(), metadata=_make_metadata(visited_order, frontier.copy(), None, 0, state_to_id, "No se encontró solución; la frontera está vacía.")))
    return steps

