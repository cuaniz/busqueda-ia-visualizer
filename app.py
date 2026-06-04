from __future__ import annotations

import importlib

import streamlit as st

from search_visualizer.algorithms import adversarial, informed, local, uninformed
from search_visualizer.problems.frozen_lake import FrozenLake
from search_visualizer.problems.sokoban import Sokoban
from search_visualizer.ui import renderers

# Streamlit reruns app.py, but imported project modules can remain cached in memory.
# Reloading them keeps the running app aligned with local code changes during development.
importlib.reload(adversarial)
importlib.reload(informed)
importlib.reload(local)
importlib.reload(uninformed)
importlib.reload(renderers)

st.set_page_config(page_title="Visualizador de búsqueda IA", layout="wide")

PROBLEMS = {
    "Búsqueda no informada — Frozen Lake determinista": ["BFS", "DFS", "UCS"],
    "Búsqueda informada — Sokoban": ["A*", "Greedy Best-First Search"],
    "Búsqueda local — 8 reinas": ["Hill Climbing", "Simulated Annealing"],
    "Búsqueda adversaria — Gato / Tic-Tac-Toe": ["Minimax", "Alpha-Beta Pruning"],
}

EXPLANATIONS = {
    "BFS": "BFS usa una cola FIFO. Expande por niveles y encuentra el camino con menor número de pasos si todos los costos son iguales.",
    "DFS": "DFS usa una pila LIFO. Profundiza primero; puede encontrar solución rápido, pero no garantiza optimalidad.",
    "UCS": "UCS usa una cola de prioridad ordenada por costo acumulado g(n). Es óptimo con costos positivos.",
    "A*": "A* combina costo acumulado y heurística: f(n)=g(n)+h(n).",
    "Greedy Best-First Search": "Greedy prioriza solo h(n). Suele ser rápido, pero puede no ser óptimo.",
    "Hill Climbing": "Hill Climbing mejora una solución completa eligiendo vecinos con menos conflictos.",
    "Simulated Annealing": "Simulated Annealing acepta a veces movimientos peores para escapar de óptimos locales.",
    "Minimax": "Minimax asume que el oponente juega óptimamente y alterna MAX/MIN.",
    "Alpha-Beta Pruning": "Alpha-Beta produce la misma decisión que Minimax, pero poda ramas que no pueden cambiar el resultado.",
}


def safe_key(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value)


def clamp_step(value: int, total: int) -> int:
    return min(max(int(value), 1), total)


def set_step(slider_key: str, total: int, value: int) -> None:
    st.session_state[slider_key] = clamp_step(value, total)


def show_step_controls(steps, context_key: str):
    if not steps:
        st.warning("No se generaron pasos.")
        return None

    total = len(steps)
    slider_key = f"step_slider_{context_key}"
    last_total_key = f"step_total_{context_key}"

    if slider_key not in st.session_state or st.session_state.get(last_total_key) != total:
        st.session_state[slider_key] = 1
        st.session_state[last_total_key] = total

    st.session_state[slider_key] = clamp_step(st.session_state[slider_key], total)
    current_step = st.session_state[slider_key]

    metric_left, metric_right = st.columns(2)
    metric_left.metric("Paso actual", f"{current_step} / {total}")
    metric_right.metric("Pasos totales", total)

    controls = st.columns(4)
    with controls[0]:
        st.button(
            "Inicio",
            disabled=current_step <= 1,
            use_container_width=True,
            key=f"{slider_key}_first",
            on_click=set_step,
            args=(slider_key, total, 1),
        )
    with controls[1]:
        st.button(
            "Retroceder",
            disabled=current_step <= 1,
            use_container_width=True,
            key=f"{slider_key}_prev",
            on_click=set_step,
            args=(slider_key, total, current_step - 1),
        )
    with controls[2]:
        st.button(
            "Avanzar",
            disabled=current_step >= total,
            use_container_width=True,
            key=f"{slider_key}_next",
            on_click=set_step,
            args=(slider_key, total, current_step + 1),
        )
    with controls[3]:
        st.button(
            "Final",
            disabled=current_step >= total,
            use_container_width=True,
            key=f"{slider_key}_last",
            on_click=set_step,
            args=(slider_key, total, total),
        )

    selected_step = st.slider("Seleccionar paso", 1, total, key=slider_key)
    current_step = clamp_step(selected_step, total)

    progress_value = min(max(current_step / total, 0.0), 1.0)
    st.progress(progress_value)

    step = steps[current_step - 1]
    st.subheader(step.title)
    st.write(step.description)
    if step.metadata:
        st.json(step.metadata)
    return step


def compact_path(path: list, formatter, max_items: int = 8) -> str:
    if len(path) <= max_items:
        return " -> ".join(formatter(item) for item in path)
    head = [formatter(item) for item in path[:3]]
    tail = [formatter(item) for item in path[-3:]]
    return " -> ".join(head + ["..."] + tail)


def show_path_summary(path: list, formatter, title: str = "Camino parcial") -> None:
    if not path:
        st.caption("Todavía no hay camino parcial para mostrar.")
        return
    st.markdown(f"**{title}: {len(path)} estado(s)**")
    st.code(compact_path(path, formatter), language="text")


def format_grid_position(position) -> str:
    return f"({position[0]}, {position[1]})"


def format_sokoban_state(state) -> str:
    player, boxes = state
    box_text = ", ".join(format_grid_position(box) for box in sorted(boxes))
    return f"P{format_grid_position(player)} | Cajas[{box_text}]"


def format_queen_board(board) -> str:
    return "[" + ", ".join(str(col) for col in board) + "]"


def run_frozen_lake(algorithm: str):
    problem = FrozenLake()
    if algorithm == "BFS":
        steps = uninformed.breadth_first_search(problem.start, problem.is_goal, problem.successors)
    elif algorithm == "DFS":
        steps = uninformed.depth_first_search(problem.start, problem.is_goal, problem.successors)
    else:
        steps = uninformed.uniform_cost_search(problem.start, problem.is_goal, problem.successors)

    left, right = st.columns([1, 1])
    with left:
        step = show_step_controls(steps, safe_key(f"frozen_{algorithm}"))
    with right:
        if step is not None:
            st.markdown(renderers.render_frozen_lake(problem, step.state, step.visited, step.frontier, step.path), unsafe_allow_html=True)
            st.caption("Colores: actual=naranja, visitado=amarillo, frontera=azul, camino parcial=verde.")
            show_path_summary(step.path, format_grid_position)


def run_sokoban(algorithm: str):
    problem = Sokoban()
    if algorithm == "A*":
        steps = informed.a_star_search(problem.start, problem.is_goal, problem.successors, problem.heuristic)
    else:
        steps = informed.greedy_best_first_search(problem.start, problem.is_goal, problem.successors, problem.heuristic)

    left, right = st.columns([1, 1])
    with left:
        step = show_step_controls(steps, safe_key(f"sokoban_{algorithm}"))
    with right:
        if step is not None:
            st.markdown(
                renderers.render_sokoban(
                    problem=problem,
                    state=step.state,
                    visited_count=len(step.visited),
                    frontier_count=len(step.frontier),
                    path=step.path,
                ),
                unsafe_allow_html=True,
            )
            st.caption("La ruta verde representa las posiciones del jugador en el camino parcial. La heurística usa distancia Manhattan de cajas a objetivos.")
            show_path_summary(step.path, format_sokoban_state)


def run_queens(algorithm: str):
    seed = st.sidebar.number_input("Semilla aleatoria", min_value=0, max_value=9999, value=7, step=1)
    start = local.random_board(seed=int(seed))
    steps = local.hill_climbing(start) if algorithm == "Hill Climbing" else local.simulated_annealing(start, seed=int(seed))

    left, right = st.columns([1, 1])
    with left:
        step = show_step_controls(steps, safe_key(f"queens_{algorithm}_{seed}"))
    with right:
        if step is not None:
            st.markdown(renderers.render_queens(step.state), unsafe_allow_html=True)
            st.metric("Conflictos", local.conflicts(step.state))
            st.caption("El objetivo es llegar a 0 conflictos entre reinas.")
            show_path_summary(step.path, format_queen_board, "Historial de configuraciones")


def board_from_preset(name: str):
    presets = {
        "Tablero vacío": (" ", " ", " ", " ", " ", " ", " ", " ", " "),
        "Partida media 1": ("X", "O", " ", " ", "X", " ", "O", " ", " "),
        "Partida media 2": ("O", " ", "X", " ", "X", " ", " ", "O", " "),
    }
    return presets[name]


def run_tictactoe(algorithm: str):
    preset = st.sidebar.selectbox("Estado inicial", ["Tablero vacío", "Partida media 1", "Partida media 2"])
    board = board_from_preset(preset)
    move, evaluations, next_board = adversarial.choose_move(board, ai_player="X", algorithm=algorithm)

    left, right = st.columns([1, 1])
    with left:
        st.subheader("Estado actual")
        st.markdown(renderers.render_tictactoe(board), unsafe_allow_html=True)
        if adversarial.winner(board):
            st.success(f"Ganador actual: {adversarial.winner(board)}")
        elif move is None:
            st.info("No hay movimientos disponibles.")
        else:
            st.write(f"Movimiento elegido por X: posición {move + 1}")
            st.markdown(renderers.render_tictactoe(next_board), unsafe_allow_html=True)

    with right:
        st.subheader("Evaluación de movimientos")
        st.write("Valor 1 = gana X, 0 = empate, -1 = pierde X si ambos juegan correctamente.")
        rows = [{"Movimiento": item.move + 1, "Valor": item.value, "Nodos evaluados": item.nodes} for item in evaluations]
        st.table(rows)
        st.caption("Alpha-Beta evalúa menos nodos que Minimax en muchos estados, manteniendo la misma decisión.")


st.title("Visualizador de algoritmos de búsqueda")
st.write("Aplicación para comparar algoritmos de búsqueda en problemas clásicos de Inteligencia Artificial.")

problem_name = st.sidebar.selectbox("Problema", list(PROBLEMS.keys()))
algorithm = st.sidebar.selectbox("Algoritmo", PROBLEMS[problem_name])

st.info(EXPLANATIONS[algorithm])

if "Frozen Lake" in problem_name:
    run_frozen_lake(algorithm)
elif "Sokoban" in problem_name:
    run_sokoban(algorithm)
elif "8 reinas" in problem_name:
    run_queens(algorithm)
else:
    run_tictactoe(algorithm)
