import tkinter as tk
from board import Connect4Board, PLAYER, AI
from ai_agent import minimax
from bayes_model import PlayerModel
from narrator import explain_move

ROWS = 6
COLUMNS = 7
CELL_SIZE = 80
NARRATION_LEVEL = "medium"

class Connect4GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4 AI 🎮")
        
        self.canvas = tk.Canvas(root, width=COLUMNS*CELL_SIZE, height=ROWS*CELL_SIZE + 100, bg="white")
        self.canvas.pack()

        self.status_text = tk.StringVar()
        self.status_label = tk.Label(root, textvariable=self.status_text, font=("Arial", 14))
        self.status_label.pack()

        self.reset_button = tk.Button(root, text="🔄 Reset Game", command=self.reset_game, font=("Arial", 12))
        self.reset_button.pack(pady=10)

        self.canvas.bind("<Button-1>", self.handle_click)

        self.reset_game()  # Initialize game state

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(ROWS):
            for col in range(COLUMNS):
                x0 = col * CELL_SIZE
                y0 = row * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue")
                piece = self.board.grid[row][col]
                color = "white"
                if piece == PLAYER:
                    color = "red"
                elif piece == AI:
                    color = "yellow"
                self.canvas.create_oval(x0+5, y0+5, x1-5, y1-5, fill=color)

    def handle_click(self, event):
        if self.board.is_full() or self.board.check_winner(PLAYER) or self.board.check_winner(AI):
            return

        col = event.x // CELL_SIZE
        if col not in self.board.valid_moves():
            return

        if self.current_player == PLAYER:
            self.board.make_move(col, PLAYER)
            self.model.record_move(col)
            self.draw_board()

            if self.board.check_winner(PLAYER):
                self.status_text.set("🏆 You win!")
                return

            self.current_player = AI
            self.root.after(500, self.ai_move)

    def ai_move(self):
        if self.board.is_full() or self.board.check_winner(PLAYER) or self.board.check_winner(AI):
            return

        self.status_text.set("🤖 AI is thinking...")
        self.root.update()

        move, _ = minimax(self.board, depth=4, alpha=float('-inf'), beta=float('inf'), maximizing_player=True, model=self.model)
        self.board.make_move(move, AI)
        self.draw_board()

        explanation = explain_move(move, self.board, self.model, verbosity=NARRATION_LEVEL)
        self.status_text.set(f"AI played column {move}. {explanation}")

        if self.board.check_winner(AI):
            self.status_text.set("💻 AI wins!")
            return

        self.current_player = PLAYER

    def reset_game(self):
        self.board = Connect4Board()
        self.model = PlayerModel()
        self.current_player = PLAYER
        self.status_text.set("Your turn (Player X)")
        self.draw_board()

def main():
    root = tk.Tk()
    app = Connect4GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
