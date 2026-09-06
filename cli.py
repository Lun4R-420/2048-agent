import time
from board import new_board, spawn_tile, game_over
from search import best_move
from tools import directions
from agent import check_milestone, agent_choose_move

def render(board):
    border = "+------" * 4 + "+"
    print(border)
    for row in board:
        line = "|"
        for value in row:
            cell = str(value) if value != 0 else ""
            line += f"{cell:^6}|"
        print(line)
        print(border)

def demo_game(depth=3):
    board = new_board()
    seen_milestones = set()
    moves_played = 0

    print("Starting board: ")
    render(board)

    while not game_over(board):
        milestone = check_milestone(board, seen_milestones)
        if milestone:
            time.sleep(5)
            direction, explanation = agent_choose_move(board, milestone)
            move_fn = directions.get(direction) if direction else None
            if move_fn is None:
                move_fn = best_move(board, depth)
            board = move_fn(board)
            spawn_tile(board)
            moves_played += 1

            print(f"\nMILESTONE {milestone}!\n")
            print(explanation)
            render(board)
            time.sleep(3)
        else:
            move_fn = best_move(board, depth)
            board = move_fn(board)
            spawn_tile(board)
            moves_played += 1

    print("\nFinal board:")
    render(board)
    max_tile = max(max(row) for row in board)
    print(f"Game over. Max tile: {max_tile}, moves played: {moves_played}")
    return max_tile, moves_played

if __name__ == "__main__":
    demo_game(3)