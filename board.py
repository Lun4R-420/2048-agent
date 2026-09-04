import random

def new_board():
    board = [[0] * 4 for _ in range(4)]
    return board

def spawn_tile(board):
    empty_tiles = []
    for row in range(4):
        for col in range(4):
            if board[row][col] == 0:
                empty_tiles.append((row, col))

    if not empty_tiles:
        return

    row, col = random.choice(empty_tiles)

    value = random.choices([2, 4], weights=(90, 10), k=1)
    board[row][col] = value[0]

def process_row_left(row):
    compressed = [value for value in row if value != 0]
    merged = []
    i = 0
    while i < len(compressed):
        if i + 1 < len(compressed) and compressed[i] == compressed[i + 1]:
            merged.append(compressed[i] + compressed[i + 1])
            i += 2
        else:
            merged.append(compressed[i])
            i += 1

    while len(merged) < 4:
        merged.append(0)
    return merged

def move_left(board):
    new_board = []
    for row in range(4):
        new_row = process_row_left(board[row])
        new_board.append(new_row)
    return new_board

def process_row_right(row):
    reversed_row = row[::-1]
    merged = process_row_left(reversed_row)
    reversed_merged = merged[::-1]
    return reversed_merged

def move_right(board):
    new_board = []
    for row in range(4):
        new_row = process_row_right(board[row])
        new_board.append(new_row)
    return new_board

def transpose(board):
    transposed = [list(col) for col in zip(*board)]
    return transposed

def move_up(board):
    transposed = transpose(board)
    new_board = []
    for col in range(4):
        new_col = process_row_left(transposed[col])
        new_board.append(new_col)
    return transpose(new_board)

def move_down(board):
    transposed = transpose(board)
    new_board = []
    for col in range(4):
        new_col = process_row_right(transposed[col])
        new_board.append(new_col)
    return transpose(new_board)

def game_over(board):
    empty = 0
    for row in range(4):
        empty += len([value for value in board[row] if value == 0])
    if empty == 16:
        return False
    moves = [move_left, move_right, move_up, move_down]
    for move in moves:
        if move(board) != board:
            return False
    return True