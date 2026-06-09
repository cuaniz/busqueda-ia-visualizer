"""Adversarial search algorithms for Tic-Tac-Toe."""

from __future__ import annotations

from dataclasses import dataclass

Board = tuple[str, ...]
WIN_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


@dataclass
class MoveEvaluation:
    move: int
    value: int
    nodes: int


def winner(board: Board) -> str | None:
    for a, b, c in WIN_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_full(board: Board) -> bool:
    return all(cell != " " for cell in board)


def available_moves(board: Board) -> list[int]:
    return [i for i, cell in enumerate(board) if cell == " "]


def play(board: Board, move: int, player: str) -> Board:
    cells = list(board)
    cells[move] = player
    return tuple(cells)


def utility(board: Board, ai_player: str) -> int:
    win = winner(board)
    if win == ai_player:
        return 1
    if win is not None:
        return -1
    return 0


def opponent(player: str) -> str:
    return "O" if player == "X" else "X"


def alpha_beta_value(board: Board, current_player: str, ai_player: str, alpha: int = -10, beta: int = 10) -> tuple[int, int]:
    win = winner(board)
    if win is not None or is_full(board):
        return utility(board, ai_player), 1

    nodes = 1
    if current_player == ai_player:
        value = -10
        for move in available_moves(board):
            child_value, child_nodes = alpha_beta_value(play(board, move, current_player), opponent(current_player), ai_player, alpha, beta)
            nodes += child_nodes
            value = max(value, child_value)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, nodes

    value = 10
    for move in available_moves(board):
        child_value, child_nodes = alpha_beta_value(play(board, move, current_player), opponent(current_player), ai_player, alpha, beta)
        nodes += child_nodes
        value = min(value, child_value)
        beta = min(beta, value)
        if alpha >= beta:
            break
    return value, nodes


def choose_move_alpha_beta(board: Board, ai_player: str = "X") -> tuple[int | None, Board | None]:
    """Select the best move for ai_player using Alpha-Beta pruning only."""
    moves = available_moves(board)
    if not moves or winner(board) is not None:
        return None, None

    best_move: int | None = None
    best_value: int = -10
    for move in moves:
        next_board = play(board, move, ai_player)
        value, _nodes = alpha_beta_value(next_board, opponent(ai_player), ai_player)
        if value > best_value:
            best_value = value
            best_move = move
    return best_move, play(board, best_move, ai_player) if best_move is not None else None
