from board import Connect4Board, ROWS, COLUMNS

def copy_board(board_obj):
    new_board = Connect4Board()
    for r in range(ROWS):
        for c in range(COLUMNS):
            new_board.grid[r][c] = board_obj.grid[r][c]
    return new_board
