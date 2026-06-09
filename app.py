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
    "Búsqueda no informada — Frozen Lake determinista": ["BFS", "DFS"],
    "Búsqueda informada — Sokoban": ["A*", "Greedy Best-First Search"],
    "Búsqueda local — 8 reinas": ["Hill Climbing", "Simulated Annealing"],
    "Búsqueda adversaria — Gato / Tic-Tac-Toe": ["Alpha-Beta Pruning"],
}

EXPLANATIONS = {
    "BFS": "BFS usa una cola FIFO. Expande por niveles y encuentra el camino con menor número de pasos si todos los costos son iguales.",
    "DFS": "DFS usa una pila LIFO. Profundiza primero; puede encontrar solución rápido, pero no garantiza optimalidad.",
    "A*": "A* combina costo acumulado y heurística: f(n)=g(n)+h(n).",
    "Greedy Best-First Search": "Greedy prioriza solo h(n). Suele ser rápido, pero puede no ser óptimo.",
    "Hill Climbing": "Hill Climbing mejora una solución completa eligiendo vecinos con menos conflictos.",
    "Simulated Annealing": "Simulated Annealing acepta a veces movimientos peores para escapar de óptimos locales.",
    "Alpha-Beta Pruning": "Alpha-Beta evalúa recursivamente estados de juego con poda para descartar ramas que no pueden cambiar el resultado.",
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
        md = step.metadata
        # BFS/DFS metadata has nodo_actual; show structured display instead of raw JSON.
        if "nodo_actual" in md:
            col_a, col_b = st.columns(2)
            with col_a:
                visitados = md.get("visitados", [])
                st.metric("Visitados", len(visitados) if isinstance(visitados, list) else visitados)
                frontera = md.get("frontera", [])
                st.metric("Frontera", len(frontera) if isinstance(frontera, list) else frontera)
            with col_b:
                st.metric("Nodo actual", md.get("nodo_actual", "-"))
                st.metric("Longitud camino", md.get("longitud_camino", 0))
            if md.get("comentario"):
                st.info(md["comentario"])
        else:
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
    to_id = lambda pos: renderers.position_id(pos, problem.width)
    if algorithm == "BFS":
        steps = uninformed.breadth_first_search(
            problem.start, problem.is_goal, problem.successors, state_to_id=to_id,
        )
    else:
        steps = uninformed.depth_first_search(
            problem.start, problem.is_goal, problem.successors, state_to_id=to_id,
        )

    left, right = st.columns([1, 1])
    with left:
        step = show_step_controls(steps, safe_key(f"frozen_{algorithm}"))
    with right:
        if step is not None:
            st.markdown(renderers.render_frozen_lake(problem, step.state, step.visited, step.frontier, step.path), unsafe_allow_html=True)
            st.caption("Colores: actual=naranja, visitado=amarillo, frontera=azul, camino parcial=verde.")
            st.caption("Criterio de selección: En caso de múltiples opciones, los nodos vecinos se evalúan y seleccionan en sentido antihorario.")

            # Structured metadata panel with numeric cell ids.
            if step.metadata:
                md = step.metadata
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Visitados", len(md.get("visitados", [])) if isinstance(md.get("visitados"), list) else md.get("visitados", 0))
                    st.metric("Frontera", len(md.get("frontera", [])) if isinstance(md.get("frontera"), list) else md.get("frontera", 0))
                with col_b:
                    st.metric("Nodo actual", md.get("nodo_actual", "-"))
                    st.metric("Longitud camino", md.get("longitud_camino", 0))
                if isinstance(md.get("visitados"), list):
                    with st.expander("IDs de celdas visitadas"):
                        st.code(md["visitados"])
                if isinstance(md.get("frontera"), list):
                    with st.expander("IDs de celdas en frontera"):
                        st.code(md["frontera"])
                if md.get("comentario"):
                    st.info(md["comentario"])

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


def run_tictactoe(algorithm: str):
    # Interactive human-vs-machine Tic-Tac-Toe using Alpha-Beta pruning only.
    # Human plays O, AI plays X. Board is stored in session state.
    if "ttt_board" not in st.session_state:
        st.session_state.ttt_board = (" ", " ", " ", " ", " ", " ", " ", " ", " ")

    board = st.session_state.ttt_board
    win = adversarial.winner(board)
    full = adversarial.is_full(board)
    game_over = win is not None or full

    st.session_state.ttt_game_over = game_over

    # Render the board as a 3x3 grid of buttons.
    cols = st.columns(3)
    for r in range(3):
        for c in range(3):
            idx = r * 3 + c
            cell_val = board[idx]
            label = f"{idx} {cell_val}" if cell_val != " " else str(idx)
            disabled = game_over or cell_val != " " or adversarial.winner(board) is not None
            btn_key = f"ttt_{idx}"
            if cols[c].button(label, key=btn_key, disabled=disabled, use_container_width=True):
                # Human plays O
                new_board = adversarial.play(board, idx, "O")
                st.session_state.ttt_board = new_board
                # AI replies with Alpha-Beta if game not over
                ai_move, ai_board = adversarial.choose_move_alpha_beta(new_board, ai_player="X")
                if ai_board is not None:
                    st.session_state.ttt_board = ai_board
                st.rerun()

    # Show game status
    if win:
        st.success(f"¡Ganador: {win}!")
    elif full:
        st.info("¡Empate!")
    else:
        moves_left = len(adversarial.available_moves(board))
        st.write(f"Turno: {'O (Humano)' if moves_left % 2 == 1 else 'X (Máquina)'} — {moves_left} movimiento(s) disponible(s)")

    st.caption("Humano = O, Máquina = X (Alpha-Beta). La máquina responde automáticamente después de cada jugada humana.")

    if st.button("Reiniciar partida", key="ttt_reset"):
        st.session_state.ttt_board = (" ", " ", " ", " ", " ", " ", " ", " ", " ")
        st.session_state.ttt_game_over = False
        st.rerun()


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
