from heuristics import evaluate
from board import move_left, move_right, move_up, move_down, game_over

def legal_moves(board):
    moves = [move_left, move_right, move_up, move_down]
    legal_moves = []
    for move in moves:
        if move(board) != board:
            legal_moves.append(move)
    return legal_moves

def expectimax(board, depth, is_player_turn):
    if depth == 0 or game_over(board):
        return evaluate(board)

    best_value = float('-inf')
    if is_player_turn:
        moves = legal_moves(board)
        if not moves:
            return evaluate(board)
        for move in moves:
            moved_board = move(board)
            result = expectimax(moved_board, depth-1, False)
            best_value = max(best_value, result)

        return best_value
    else:
        empty_cells = [(r, c) for r in range(4) for c in range(4) if board[r][c] == 0]

        total = 0
        for (r, c) in empty_cells:
            for value, prob in [(2, 0.9), (4, 0.1)]:
                board_copy = [row[:] for row in board]
                board_copy[r][c] = value
                result = expectimax(board_copy, depth-1, True)
                total += result * prob

        return total / len(empty_cells)

def best_move(board, depth):
    moves = legal_moves(board)
    max_result = float('-inf')
    optimal_move = None
    
    for move in moves:
        moved_board = move(board)
        result = expectimax(moved_board, depth-1, False)
        if result > max_result:
            max_result = result
            optimal_move = move
    return optimal_move