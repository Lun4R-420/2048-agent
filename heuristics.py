from board import transpose
import math

WEIGHTS = [1, 1, -1, 1]

def count_empty(board) -> int:
    count = 0
    for row in range(4):
        count += len([value for value in board[row] if value == 0])
    return count

def monotonicity(board):
    pairs = [] # -1 for decreasing, 1 for increasing
    for row in board:
        increasing = 0
        decreasing = 0
        for i in range(len(row) - 1):
            if row[i] < row[i + 1]:
                increasing += 1
            elif row[i] > row[i + 1]:
                decreasing += 1
        if increasing > decreasing:
            pairs.append(1)
        elif increasing < decreasing:
            pairs.append(-1)
    transposed_board = transpose(board)
    for col in transposed_board:
        increasing = 0
        decreasing = 0
        for i in range(len(col) - 1):
            if col[i] < col[i + 1]:
                increasing += 1
            elif col[i] > col[i + 1]:
                decreasing += 1
        if increasing > decreasing:
            pairs.append(1)
        elif increasing < decreasing:
            pairs.append(-1)
    return abs(sum(pairs))

def smoothness(board):
    smooth = 0
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                continue
            if i + 1 < 4 and board[i + 1][j] != 0:
                smooth += abs(math.log2(board[i][j]) - math.log2(board[i + 1][j]))
            if j + 1 < 4 and board[i][j + 1] != 0:
                smooth += abs(math.log2(board[i][j]) - math.log2(board[i][j + 1]))

    return smooth

def corner_weight(board):
    maximum = max(board[0][0], board[0][3], board[3][0], board[3][3])
    if maximum == 0:
        return 0
    return math.log2(maximum)

def evaluate(board):
    heuristics = [count_empty(board), monotonicity(board), smoothness(board), corner_weight(board)]
    return sum([WEIGHTS[i] * heuristics[i] for i in range(4)])