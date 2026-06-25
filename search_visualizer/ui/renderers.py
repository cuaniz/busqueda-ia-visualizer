

from __future__ import annotations

from html import escape
from typing import Iterable

from search_visualizer.problems.frozen_lake import FrozenLake, Position
from search_visualizer.problems.sokoban import Sokoban, SokobanState

ICON_SIZE = 28


def cell_id(row: int, col: int, width: int) -> int:
    return row * width + col


def position_id(pos: tuple[int, int], width: int) -> int:
    return pos[0] * width + pos[1]


def _svg(body: str, view_box: str = "0 0 32 32") -> str:
    return f"<svg width='{ICON_SIZE}' height='{ICON_SIZE}' viewBox='{view_box}' aria-hidden='true' style='display:block;margin:auto'>{body}</svg>"


START_ICON = _svg("<path d='M9 6v20l17-10L9 6z' fill='#1F4E5F'/>")
TARGET_ICON = _svg("<circle cx='16' cy='16' r='10' fill='none' stroke='#3A7D44' stroke-width='3'/><circle cx='16' cy='16' r='4' fill='#3A7D44'/><path d='M16 2v6M16 24v6M2 16h6M24 16h6' stroke='#3A7D44' stroke-width='2' stroke-linecap='round'/>")
HAZARD_ICON = _svg("<path d='M8 8l16 16M24 8L8 24' stroke='#F7F4EC' stroke-width='4' stroke-linecap='round'/>")
FLOOR_ICON = _svg("<circle cx='16' cy='16' r='3' fill='#A0A090'/>")
CURRENT_ICON = _svg("<circle cx='16' cy='16' r='10' fill='#C69C3D'/><circle cx='16' cy='16' r='4' fill='#FFFDF5'/>")
PATH_ICON = _svg("<circle cx='16' cy='16' r='6' fill='#3A7D44'/><path d='M6 16h20' stroke='#3A7D44' stroke-width='3' stroke-linecap='round' opacity='0.55'/>")
FRONTIER_ICON = _svg("<circle cx='16' cy='16' r='8' fill='none' stroke='#1F4E5F' stroke-width='3'/>")
WALL_ICON = _svg("<rect x='5' y='7' width='22' height='18' rx='2' fill='#6B6050'/><path d='M5 13h22M5 19h22M12 7v6M20 13v6M12 19v6' stroke='#9C9080' stroke-width='1.5'/>")
BOX_ICON = _svg("<rect x='7' y='7' width='18' height='18' rx='3' fill='#C69C3D'/><path d='M7 13h18M13 7v18' stroke='#FFFDF5' stroke-width='2'/>")
BOX_ON_TARGET_ICON = _svg("<rect x='7' y='7' width='18' height='18' rx='3' fill='#3A7D44'/><path d='M10 17l4 4 8-10' fill='none' stroke='#E6F0E8' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/>")
PLAYER_ICON = _svg("<circle cx='16' cy='10' r='5' fill='#C69C3D'/><path d='M8 27c1.5-6 5-9 8-9s6.5 3 8 9' fill='#C69C3D'/>")
QUEEN_ICON = _svg("<path d='M7 24h18l-2-12-5 5-2-8-2 8-5-5-2 12z' fill='#5C2018'/><rect x='8' y='24' width='16' height='3' rx='1.5' fill='#5C2018'/>")


def _cell(content: str, background: str = "#FFFFFF", color: str = "#1F4E5F", cell_id: int | None = None) -> str:
    badge = ""
    if cell_id is not None:
        badge = (
            "<span style='position:absolute;top:1px;left:2px;font-size:9px;"
            f"font-weight:600;color:#7A7A6A;line-height:1;pointer-events:none'>"
            f"{cell_id}</span>"
        )
    return (
        "<td style='position:relative;width:52px;height:52px;text-align:center;vertical-align:middle;"
        f"font-size:18px;font-weight:700;background:{background};color:{color};"
        "border:1px solid #D5D0C5;border-radius:50%;box-shadow:0 1px 2px rgba(0,0,0,0.06)'>"
        f"{badge}{content}</td>"
    )


def _table(rows: list[str]) -> str:
    return "<table style='border-collapse:separate;border-spacing:4px;margin:8px 0'>" + "".join(f"<tr>{row}</tr>" for row in rows) + "</table>"


def render_frozen_lake(
    problem: FrozenLake,
    current: Position | None,
    visited: set[Position] | None = None,
    frontier: Iterable[Position] | None = None,
    path: list[Position] | None = None,
) -> str:
    visited = visited or set()
    frontier_set = set(frontier or [])
    path_set = set(path or [])
    rows = []
    for r, row in enumerate(problem.grid):
        cells = []
        for c, value in enumerate(row):
            pos = (r, c)
            content = {"S": START_ICON, "G": TARGET_ICON, "H": HAZARD_ICON, "F": FLOOR_ICON}.get(value, escape(value))
            background = "#FFFFFF"
            color = "#1F4E5F"
            if value == "H":
                background = "#A94438"
                color = "#F7F4EC"
            if pos in visited:
                background = "#F0EBDA"
            if pos in frontier_set:
                background = "#D6E6EB"
                content = FRONTIER_ICON if value == "F" else content
            if pos in path_set:
                background = "#D9E8D9"
                content = PATH_ICON if value == "F" else content
            if current == pos:
                content = CURRENT_ICON
                background = "#FDF3E0"
            cells.append(_cell(content, background, color, cell_id=r * problem.width + c))
        rows.append("".join(cells))
    return _table(rows)


def render_sokoban(
    problem: Sokoban,
    state: SokobanState | None,
    visited_count: int = 0,
    frontier_count: int = 0,
    path: list[SokobanState] | None = None,
) -> str:
    if state is None:
        return "<p>No hay estado para mostrar.</p>"
    player, boxes = state
    player_path = {item[0] for item in path or [] if item is not None}
    rows = []
    for r, row in enumerate(problem.grid):
        cells = []
        for c, _value in enumerate(row):
            pos = (r, c)
            content = FLOOR_ICON
            background = "#FFFFFF"
            if pos in player_path:
                background = "#D9E8D9"
                content = PATH_ICON
            if pos in problem.walls:
                content = WALL_ICON
                background = "#E0DBD0"
            elif pos in problem.goals and pos in boxes:
                content = BOX_ON_TARGET_ICON
                background = "#D9E8D9"
            elif pos in problem.goals:
                content = TARGET_ICON
                background = "#E6F0E8"
            elif pos in boxes:
                content = BOX_ICON
                background = "#FDF3E0"
            if pos == player:
                content = PLAYER_ICON
                background = "#FDF3E0"
            cells.append(_cell(content, background, "#1F4E5F", cell_id=r * problem.width + c))
        rows.append("".join(cells))
    stats = f"<p><strong>Visitados:</strong> {visited_count} | <strong>Frontera:</strong> {frontier_count}</p>"
    return _table(rows) + stats


def render_queens(board: tuple[int, ...]) -> str:
    n = len(board)
    rows = []
    for r in range(n):
        label_cell = (
            "<td style='width:24px;height:52px;text-align:center;vertical-align:middle;"
            f"font-size:13px;font-weight:700;color:#5C6B6F;border:none'>{r + 1}</td>"
        )
        cells = [label_cell]
        for c in range(n):
            has_queen = board[r] == c
            background = "#FFFFFF" if (r + c) % 2 == 0 else "#F0EBDA"
            cells.append(_cell(QUEEN_ICON if has_queen else "", background, "#5C2018", cell_id=r * n + c))
        rows.append("".join(cells))
    return _table(rows)


def render_tictactoe(board: tuple[str, ...]) -> str:
    rows = []
    for r in range(3):
        cells = []
        for c in range(3):
            value = board[r * 3 + c]
            content = escape(value) if value != " " else "&nbsp;"
            background = "#D6E6EB" if value == "X" else "#F5E4E2" if value == "O" else "#FFFFFF"
            color = "#1F4E5F" if value == "X" else "#A94438" if value == "O" else "#1F4E5F"
            cells.append(_cell(content, background, color, cell_id=r * 3 + c))
        rows.append("".join(cells))
    return _table(rows)
