from board import Connect4Board, PLAYER, AI
from ai_agent import minimax
from bayes_model import PlayerModel
from narrator import explain_move

#You can adjust the verbosity of the AI's explanations. Look at the options below:
# Options: "short", "medium", "long"
NARRATION_LEVEL = "medium"



def main():

    with open("data/ai_log.txt", "w") as log_file:
        log_file.write("📝 AI Move Log\n")
        log_file.write("====================\n")
        
    board = Connect4Board()
    model = PlayerModel()
    current_player = PLAYER

    print("🎮 Welcome to Connect 4!")
    board.print_board()

    while not board.is_full():
        print(f"\n{'Player (X)' if current_player == PLAYER else 'AI (O)'}'s turn")

        if current_player == PLAYER:
            try:
                move = int(input("Enter column number (0–6): "))
            except ValueError:
                print("⚠️ Invalid input. Please enter a number between 0 and 6.")
                continue

            if move not in board.valid_moves():
                print("🚫 That column is full or invalid. Try a different one.")
                continue

            model.record_move(move)

            print(f"🤖 Prediction: Player favors column {model.most_likely_column()}")

        else:
            print("AI is thinking...")
            move, _ = minimax(board, depth=4, alpha=float('-inf'), beta=float('inf'), maximizing_player=True, model=model)
            explaination = explain_move(move, board, model, verbosity=NARRATION_LEVEL)
            print(f"AI chose column {move}. {explaination}")

            with open("data/ai_move_log.txt", "a") as log_file:
                log_file.write(f"AI played column {move}. {explaination}\n")

        board.make_move(move, current_player)
        board.print_board()

        if board.check_winner(current_player):
            print(f"\n🏆 {'Player (X)' if current_player == PLAYER else 'AI (O)'} wins!")
            return

        current_player = AI if current_player == PLAYER else PLAYER

    print("🤝 Game over — It's a draw!")

    #print("Press Ctrl+C to quit at any time.\n")


if __name__ == "__main__":
    main()

