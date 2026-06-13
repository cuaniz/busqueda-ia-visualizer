from __future__ import annotations

import importlib

import streamlit as st

from search_visualizer.algorithms import adversarial, informed, local, uninformed
from search_visualizer.problems.frozen_lake import FrozenLake
from search_visualizer.problems.sokoban import Sokoban
from search_visualizer.ui import renderers

importlib.reload(adversarial)
importlib.reload(informed)
importlib.reload(local)
importlib.reload(uninformed)
importlib.reload(renderers)

st.set_page_config(
    page_title="Laboratorio de Algoritmos de Búsqueda — IA",
    layout="wide",
    page_icon="🔬",
    initial_sidebar_state="collapsed",
)

# ── Identidad visual: Laboratorio Académico — Paleta Armónica ───────────────
st.markdown(
    """
<style>
    :root {
        --lab-bg: #F7F3EA;
        --lab-card-bg: #FFFFFF;
        --lab-border: #E8E1D0;
        --lab-primary: #3A6B7C;
        --lab-primary-hover: #4A7B8C;
        --lab-primary-dark: #2C5A6B;
        --lab-text: #6B7B7D;
        --lab-muted: #8A8A7A;
        --lab-accent: #C9A86A;
        --lab-success: #6B8E5A;
        --lab-error: #A06868;
        --lab-info-bg: #EEF3F5;
        --lab-success-bg: #EEF3E8;
        --lab-warning-bg: #F5EFE0;
        --lab-error-bg: #F5EAE8;
    }

    .stApp { background-color: var(--lab-bg); }
    .main .block-container { padding-top: 1rem; max-width: 1500px; }

    /* ── Header slim ── */
    .lab-header-slim {
        padding: 0.55rem 0.4rem 0.45rem 0.4rem;
        margin-bottom: 0.7rem;
        border-bottom: 2px solid var(--lab-primary);
    }
    .lab-header-slim h1 {
        margin: 0;
        font-size: 1.35rem;
        color: var(--lab-primary-dark);
        font-weight: 700;
        letter-spacing: -0.2px;
    }
    .lab-header-slim p {
        margin: 0.12rem 0 0 0;
        font-size: 0.8rem;
        color: var(--lab-text);
    }

    /* ── Tarjetas via st.container(border=True) ── */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: var(--lab-card-bg);
        border-radius: 8px;
        border: 1px solid var(--lab-border) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        padding: 0.75rem 1rem;
        margin-bottom: 0.7rem;
    }
    .lab-section-title {
        color: var(--lab-primary-dark);
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin: 0 0 0.45rem 0;
        border-bottom: 1.5px solid var(--lab-accent);
        padding-bottom: 0.22rem;
    }

    /* ── Descripción compacta ── */
    .lab-description {
        color: var(--lab-text);
        font-size: 0.85rem;
        font-style: italic;
        padding: 0.35rem 0.7rem;
        margin: 0 0 0.7rem 0;
        border-left: 3px solid var(--lab-accent);
        background-color: var(--lab-warning-bg);
        border-radius: 0 4px 4px 0;
    }

    /* ── Sidebar oculto ── */
    section[data-testid="stSidebar"] { display: none; }
    [data-testid="collapsedControl"] { display: none; }

    /* ── Selectbox / number input (override dark default) ── */
    .stSelectbox label, .stNumberInput label {
        color: var(--lab-primary-dark) !important;
        font-weight: 700;
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 0.4px;
        margin-bottom: 0.15rem;
    }
    .stSelectbox [data-baseweb="select"] {
        background-color: var(--lab-card-bg) !important;
    }
    .stSelectbox [data-baseweb="select"] > div {
        background-color: var(--lab-card-bg) !important;
        color: var(--lab-primary-dark) !important;
        border-color: var(--lab-border) !important;
    }
    .stSelectbox [data-baseweb="select"] > div > div,
    .stSelectbox [data-baseweb="select"] > div > div > div,
    .stSelectbox [data-baseweb="select"] span {
        color: var(--lab-primary-dark) !important;
        background-color: transparent !important;
    }
    .stSelectbox input {
        color: var(--lab-primary-dark) !important;
        caret-color: var(--lab-primary-dark) !important;
    }
    .stNumberInput input {
        background-color: var(--lab-card-bg) !important;
        color: var(--lab-primary-dark) !important;
        border-color: var(--lab-border) !important;
    }
    .stNumberInput button {
        background-color: var(--lab-primary) !important;
        color: #FFFFFF !important;
        border: none !important;
    }
    .stNumberInput button:hover {
        background-color: var(--lab-primary-hover) !important;
    }
    .stNumberInput button svg {
        fill: #FFFFFF !important;
    }

    /* ── Métricas ── */
    div[data-testid="stMetric"] {
        background-color: var(--lab-bg);
        border: 1px solid var(--lab-border);
        border-radius: 6px;
        padding: 0.45rem 0.65rem;
    }
    div[data-testid="stMetric"] label {
        color: var(--lab-text) !important;
        font-size: 0.66rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: var(--lab-primary-dark) !important;
        font-size: 1.05rem;
        font-weight: 700;
    }

    /* ── Botones ── */
    .stButton > button {
        background-color: var(--lab-primary);
        color: #FFFFFF;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.78rem;
        padding: 0.32rem 0.5rem;
    }
    .stButton > button:hover { background-color: var(--lab-primary-hover); }
    .stButton > button:disabled {
        background-color: #C8D4D9;
        color: #3A4A4C;
    }

    /* ── Callouts ── */
    div[data-testid="stInfo"] {
        background-color: var(--lab-info-bg);
        border-left: 3px solid var(--lab-primary);
        padding: 0.45rem 0.75rem;
    }
    div[data-testid="stSuccess"] {
        background-color: var(--lab-success-bg);
        border-left: 3px solid var(--lab-success);
        padding: 0.45rem 0.75rem;
    }
    div[data-testid="stWarning"] {
        background-color: var(--lab-warning-bg);
        border-left: 3px solid var(--lab-accent);
        padding: 0.45rem 0.75rem;
    }
    div[data-testid="stError"] {
        background-color: var(--lab-error-bg);
        border-left: 3px solid var(--lab-error);
        padding: 0.45rem 0.75rem;
    }

    .stProgress > div > div { background-color: var(--lab-border) !important; }
    .stProgress > div > div > div { background-color: var(--lab-primary) !important; }

    div[data-testid="stSlider"] label {
        color: var(--lab-primary-dark) !important;
        font-weight: 700;
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    div[data-testid="stSlider"] [data-baseweb="slider"] > div > div {
        background-color: var(--lab-primary) !important;
    }

    .stCaption {
        color: var(--lab-text);
        font-size: 0.8rem;
        font-weight: 500;
    }

    .streamlit-expanderHeader {
        color: var(--lab-primary-dark) !important;
        font-weight: 600;
        font-size: 0.8rem;
    }

    .stCodeBlock { border-radius: 6px; }

    div[data-testid="stCodeBlock"] {
        background-color: var(--lab-info-bg) !important;
        border: 1px solid var(--lab-border) !important;
    }
    div[data-testid="stCodeBlock"] pre,
    div[data-testid="stCodeBlock"] code,
    div[data-testid="stCodeBlock"] span {
        background-color: transparent !important;
        color: var(--lab-primary-dark) !important;
    }

    h1, h2, h3 { color: var(--lab-primary-dark) !important; }
</style>
""",
    unsafe_allow_html=True,
)

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

    m1, m2 = st.columns(2)
    m1.metric("Paso actual", f"{current_step} / {total}")
    m2.metric("Pasos totales", total)

    c1, c2, c3, c4 = st.columns(4)
    c1.button("Inicio", disabled=current_step <= 1, use_container_width=True,
              key=f"{slider_key}_first", on_click=set_step, args=(slider_key, total, 1))
    c2.button("Retroceder", disabled=current_step <= 1, use_container_width=True,
              key=f"{slider_key}_prev", on_click=set_step, args=(slider_key, total, current_step - 1))
    c3.button("Avanzar", disabled=current_step >= total, use_container_width=True,
              key=f"{slider_key}_next", on_click=set_step, args=(slider_key, total, current_step + 1))
    c4.button("Final", disabled=current_step >= total, use_container_width=True,
              key=f"{slider_key}_last", on_click=set_step, args=(slider_key, total, total))

    st.slider("Seleccionar paso", 1, total, key=slider_key)
    current_step = clamp_step(st.session_state[slider_key], total)
    st.progress(min(max(current_step / total, 0.0), 1.0))
    return steps[current_step - 1]


def show_trazabilidad(step) -> None:
    md = step.metadata or {}
    visitados = md.get("visitados", [])
    frontera = md.get("frontera", [])
    visitados_count = len(visitados) if isinstance(visitados, list) else visitados
    frontera_count = len(frontera) if isinstance(frontera, list) else frontera

    a, b = st.columns(2)
    a.metric("Visitados", visitados_count)
    a.metric("Frontera", frontera_count)
    b.metric("Nodo actual", md.get("nodo_actual", "-"))
    b.metric("Longitud camino", md.get("longitud_camino", 0))

    if isinstance(visitados, list) and visitados:
        with st.expander("IDs de celdas visitadas"):
            st.code(visitados)
    if isinstance(frontera, list) and frontera:
        with st.expander("IDs de celdas en frontera"):
            st.code(frontera)
    if md.get("comentario"):
        st.info(md["comentario"])


def compact_path(path: list, formatter, max_items: int = 8) -> str:
    if len(path) <= max_items:
        return " -> ".join(formatter(item) for item in path)
    head = [formatter(item) for item in path[:3]]
    tail = [formatter(item) for item in path[-3:]]
    return " -> ".join(head + ["..."] + tail)


def show_camino(step, formatter, title: str = "Camino parcial") -> None:
    path = step.path
    if not path:
        st.caption("Todavía no hay camino parcial para mostrar.")
        return
    st.markdown(f"**{title}:** {len(path)} estado(s)")
    st.code(compact_path(path, formatter), language="text")


def format_grid_position(position) -> str:
    return f"({position[0]}, {position[1]})"


def format_sokoban_state(state) -> str:
    player, boxes = state
    box_text = ", ".join(format_grid_position(box) for box in sorted(boxes))
    return f"P{format_grid_position(player)} | Cajas[{box_text}]"


def format_queen_board(board) -> str:
    return "[" + ", ".join(str(col) for col in board) + "]"


def render_board(problem, step, problem_name: str) -> None:
    if "Frozen Lake" in problem_name:
        st.markdown(
            renderers.render_frozen_lake(problem, step.state, step.visited, step.frontier, step.path),
            unsafe_allow_html=True,
        )
        st.caption(
            "Actual = mostaza · Visitado = beige · Frontera = celeste petrol · "
            "Camino parcial = verde académico."
        )
        st.caption(
            "Criterio de selección: en caso de múltiples opciones, los nodos vecinos "
            "se evalúan y seleccionan en sentido antihorario."
        )
    elif "Sokoban" in problem_name:
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
        st.caption(
            "La ruta verde representa las posiciones del jugador en el camino parcial. "
            "Heurística = distancia Manhattan de cajas a objetivos."
        )


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
    return problem, steps


def run_sokoban(algorithm: str):
    problem = Sokoban()
    if algorithm == "A*":
        steps = informed.a_star_search(
            problem.start, problem.is_goal, problem.successors, problem.heuristic,
        )
    else:
        steps = informed.greedy_best_first_search(
            problem.start, problem.is_goal, problem.successors, problem.heuristic,
        )
    return problem, steps


def run_queens(algorithm: str, seed: int):
    start = local.random_board(seed=int(seed))
    if algorithm == "Hill Climbing":
        steps = local.hill_climbing(start)
    else:
        steps = local.simulated_annealing(start, seed=int(seed))
    return None, steps


def run_tictactoe(_algorithm: str):
    if "ttt_board" not in st.session_state:
        st.session_state.ttt_board = (" ",) * 9
    board = st.session_state.ttt_board
    win = adversarial.winner(board)
    full = adversarial.is_full(board)
    game_over = win is not None or full
    st.session_state.ttt_game_over = game_over

    cols = st.columns(3)
    for r in range(3):
        for c in range(3):
            idx = r * 3 + c
            cell_val = board[idx]
            label = f"{idx} {cell_val}" if cell_val != " " else str(idx)
            disabled = game_over or cell_val != " " or win is not None
            if cols[c].button(label, key=f"ttt_{idx}", disabled=disabled, use_container_width=True):
                new_board = adversarial.play(board, idx, "O")
                _, ai_board = adversarial.choose_move_alpha_beta(new_board, ai_player="X")
                st.session_state.ttt_board = ai_board if ai_board is not None else new_board
                st.rerun()

    if win:
        st.success(f"¡Ganador: {win}!")
    elif full:
        st.info("¡Empate!")
    else:
        moves_left = len(adversarial.available_moves(board))
        st.markdown(
            f"**Turno:** {'O (Humano)' if moves_left % 2 == 1 else 'X (Máquina)'} "
            f"&nbsp;—&nbsp; {moves_left} movimiento(s) disponible(s)"
        )
    st.caption(
        "Humano = O, Máquina = X (Alpha-Beta). La máquina responde automáticamente "
        "después de cada jugada humana."
    )
    if st.button("Reiniciar partida", key="ttt_reset"):
        st.session_state.ttt_board = (" ",) * 9
        st.session_state.ttt_game_over = False
        st.rerun()


# ── HEADER SLIM ─────────────────────────────────────────────────────────────
st.markdown(
    '<div class="lab-header-slim">'
    "<h1>🔬 Laboratorio de Algoritmos de Búsqueda</h1>"
    "<p>Visualizador interactivo para problemas clásicos de Inteligencia Artificial</p>"
    "</div>",
    unsafe_allow_html=True,
)

# ── CONFIGURACIÓN EXPERIMENTAL ───────────────────────────────────────────────
with st.container(border=True):
    st.markdown(
        '<div class="lab-section-title">Configuración experimental</div>',
        unsafe_allow_html=True,
    )
    cfg_a, cfg_b, cfg_c = st.columns([1.4, 1.4, 1])
    with cfg_a:
        problem_name = st.selectbox("Problema", list(PROBLEMS.keys()), key="problem_select")
    with cfg_b:
        algorithm = st.selectbox("Algoritmo", PROBLEMS[problem_name], key="algorithm_select")
    with cfg_c:
        if "8 reinas" in problem_name:
            st.number_input(
                "Semilla aleatoria", min_value=0, max_value=9999, value=7, step=1, key="queens_seed",
            )
        else:
            st.markdown("&nbsp;", unsafe_allow_html=True)

# ── DESCRIPCIÓN COMPACTA ────────────────────────────────────────────────────
st.markdown(
    f'<div class="lab-description">{EXPLANATIONS[algorithm]}</div>',
    unsafe_allow_html=True,
)

# ── SIMULACIÓN ───────────────────────────────────────────────────────────────
if "Frozen Lake" in problem_name or "Sokoban" in problem_name:
    if "Frozen Lake" in problem_name:
        problem, steps = run_frozen_lake(algorithm)
    else:
        problem, steps = run_sokoban(algorithm)
    ctx = safe_key(f"{problem_name}_{algorithm}")

    with st.container(border=True):
        st.markdown(
            '<div class="lab-section-title">Panel de control y simulación</div>',
            unsafe_allow_html=True,
        )
        ctrl_col, board_col = st.columns([0.8, 1.5])
        with ctrl_col:
            step = show_step_controls(steps, ctx)
        with board_col:
            if step is not None:
                render_board(problem, step, problem_name)

    if step is not None:
        tra_col, cam_col = st.columns(2)
        with tra_col:
            with st.container(border=True):
                st.markdown(
                    '<div class="lab-section-title">Trazabilidad</div>',
                    unsafe_allow_html=True,
                )
                show_trazabilidad(step)
        with cam_col:
            with st.container(border=True):
                st.markdown(
                    '<div class="lab-section-title">Camino parcial</div>',
                    unsafe_allow_html=True,
                )
                if "Frozen Lake" in problem_name:
                    show_camino(step, format_grid_position)
                else:
                    show_camino(step, format_sokoban_state)

elif "8 reinas" in problem_name:
    seed = int(st.session_state.get("queens_seed", 7))
    _, steps = run_queens(algorithm, seed)
    ctx = safe_key(f"queens_{algorithm}_{seed}")

    with st.container(border=True):
        st.markdown(
            '<div class="lab-section-title">Panel de control y simulación</div>',
            unsafe_allow_html=True,
        )
        ctrl_col, board_col = st.columns([0.8, 1.5])
        with ctrl_col:
            step = show_step_controls(steps, ctx)
        with board_col:
            if step is not None:
                st.markdown(renderers.render_queens(step.state), unsafe_allow_html=True)
                st.metric("Conflictos", local.conflicts(step.state))
                st.caption("El objetivo es llegar a 0 conflictos entre reinas.")

    if step is not None:
        tra_col, cam_col = st.columns(2)
        with tra_col:
            with st.container(border=True):
                st.markdown(
                    '<div class="lab-section-title">Trazabilidad</div>',
                    unsafe_allow_html=True,
                )
                show_trazabilidad(step)
        with cam_col:
            with st.container(border=True):
                st.markdown(
                    '<div class="lab-section-title">Historial de configuraciones</div>',
                    unsafe_allow_html=True,
                )
                show_camino(step, format_queen_board, "Historial de configuraciones")

else:
    with st.container(border=True):
        st.markdown(
            '<div class="lab-section-title">Entorno interactivo</div>',
            unsafe_allow_html=True,
        )
        run_tictactoe(algorithm)
