ROWS = 6
COLUMNS = 7
EMPTY = 0
PLAYER = 1
AI = 2

class Connect4Board:
    def __init__(self):
        self.grid = [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]

    def print_board(self):
        for row in self.grid:
            print("|", end="")
            for cell in row:
                if cell == EMPTY:
                    symbol = " "
                elif cell == PLAYER:
                    symbol = "X"
                else:
                    symbol = "O"
                print(f"{symbol}|", end="")
            print()
        print("-" * (COLUMNS * 2 + 1))
        print(" " + " ".join(str(i) for i in range(COLUMNS)))

    def make_move(self, col, player):
        if col < 0 or col >= COLUMNS:
            return False 

        for row in reversed(range(ROWS)):
            if self.grid[row][col] == EMPTY:
                self.grid[row][col] = player
                return True

        return False 

    def valid_moves(self):
        return [col for col in range(COLUMNS) if self.grid[0][col] == EMPTY]

    def is_full(self):
        return all(cell != EMPTY for cell in self.grid[0])

    def check_winner(self, player):
        for row in range(ROWS):
            for col in range(COLUMNS - 4 + 1):
                if all(self.grid[row][col + i] == player for i in range(4)):
                    return True

        for col in range(COLUMNS):
            for row in range(ROWS - 4 + 1):
                if all(self.grid[row + i][col] == player for i in range(4)):
                    return True

        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                if all(self.grid[row + i][col + i] == player for i in range(4)):
                    return True

        for row in range(3, ROWS):
            for col in range(COLUMNS - 3):
                if all(self.grid[row - i][col + i] == player for i in range(4)):
                    return True

        return False
