from board import move_left, move_right, move_up, move_down
from search import legal_moves, expectimax

directions = {
    "left": move_left,
    "right": move_right,
    "up": move_up,
    "down": move_down
}

def get_valid_moves(board) -> list[str]:
    legal = legal_moves(board)
    valid_moves = []
    for legal_move in legal:
        for name, move_fn in directions.items():
            if move_fn == legal_move:
                valid_moves.append(name)
    return valid_moves

def evaluate_board(board, direction) -> float:
    if direction not in directions:
        return None

    valid_moves = get_valid_moves(board)
    if direction not in valid_moves:
        return float('-inf')

    move_fn = directions[direction]
    moved_board = move_fn(board)
    result = expectimax(moved_board, 3, False)
    return result 