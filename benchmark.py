from board import new_board, spawn_tile, game_over
from search import best_move

def play_game(depth):
    board = new_board()
    moves_played = 0
    while not game_over(board):
        move = best_move(board, depth)
        board = move(board)
        moves_played += 1
        spawn_tile(board)
    max_tile = max(max(row) for row in board)
    return (max_tile, moves_played)

def run_benchmark(num_games, depth):
    wins = 0
    average_max_tile = 0
    average_moves_played = 0
    for _ in range(num_games):
        max_tile, moves_played = play_game(depth)
        if max_tile >= 2048:
            wins += 1
        average_max_tile += max_tile
        average_moves_played += moves_played
    win_rate = wins / num_games
    average_max_tile /= num_games
    average_moves_played /= num_games
    return (win_rate, average_max_tile, average_moves_played)

if __name__ == "__main__":
    win_rate, average_max_tile, average_moves_played = run_benchmark(100, 3)
    print(f"Win Rate: {win_rate}, Average Max Tile: {average_max_tile}, Average Number of Moves Played: {average_moves_played}")

# Stats before tuning the heuristic weights:
# Win Rate: 0.38, Average Max Tile: 1332.48, Average Number of Moves Played: 1092.05