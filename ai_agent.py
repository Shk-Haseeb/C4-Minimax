
import random
from board import ROWS, COLUMNS, EMPTY, PLAYER, AI

def evaluate_window(window, player):
    score = 0
    opponent = PLAYER if player == AI else AI

    if window.count(player) == 4:
        score += 1000
    elif window.count(player) == 3 and window.count(0) == 1:
        score += 100
    elif window.count(player) == 2 and window.count(0) == 2:
        score += 10

    if window.count(opponent) == 3 and window.count(0) == 1:
        score -= 80 

    return score

def evaluate_board(board_obj, player):
    score = 0
    grid = board_obj.grid

    center_col = [grid[row][COLUMNS // 2] for row in range(ROWS)]
    center_count = center_col.count(player)
    score += center_count * 6

    for row in range(ROWS):
        row_array = grid[row]
        for col in range(COLUMNS - 3):
            window = row_array[col:col+4]
            score += evaluate_window(window, player)

    for col in range(COLUMNS):
        col_array = [grid[row][col] for row in range(ROWS)]
        for row in range(ROWS - 3):
            window = col_array[row:row+4]
            score += evaluate_window(window, player)

    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            window = [grid[row+i][col+i] for i in range(4)]
            score += evaluate_window(window, player)

    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            window = [grid[row-i][col+i] for i in range(4)]
            score += evaluate_window(window, player)

    return score

def minimax(board_obj, depth, alpha, beta, maximizing_player):
    valid_cols = board_obj.valid_moves()

    is_terminal = board_obj.check_winner(PLAYER) or board_obj.check_winner(AI) or board_obj.is_full()
    if depth == 0 or is_terminal:
        if board_obj.check_winner(AI):
            return (None, 1000000)
        elif board_obj.check_winner(PLAYER):
            return (None, -1000000)
        else:
            return (None, evaluate_board(board_obj, AI))

    if maximizing_player:
        value = float('-inf')
        best_col = valid_cols[0]
        for col in valid_cols:
            temp_board = copy_board(board_obj)
            temp_board.make_move(col, AI)
            _, score = minimax(temp_board, depth - 1, alpha, beta, False)
            if score > value:
                value = score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break 
        return best_col, value
    else:
        value = float('inf')
        best_col = valid_cols[0]
        for col in valid_cols:
            temp_board = copy_board(board_obj)
            temp_board.make_move(col, PLAYER)
            _, score = minimax(temp_board, depth - 1, alpha, beta, True)
            if score < value:
                value = score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value


def copy_board(board_obj):
    from board import Connect4Board
    new_board = Connect4Board()
    for r in range(ROWS):
        for c in range(COLUMNS):
            new_board.grid[r][c] = board_obj.grid[r][c]
    return new_board
