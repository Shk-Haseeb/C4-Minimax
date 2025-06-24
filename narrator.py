import random
from board import PLAYER, AI

def explain_move(move, board_obj, model=None, verbosity="medium"):
    explanation = []

    center_col = len(board_obj.grid[0]) // 2
    if move == center_col:
        explanation.append(random.choice([
            "I prefer the center column — it's strategic.",
            "The center gives me more control.",
            "I like playing the center early on."
        ]))

    if model:
        player_fav = model.most_likely_column()
        if move == player_fav:
            explanation.append(random.choice([
                f"I've seen you favor column {move}, so I played there defensively.",
                f"You keep choosing column {move}, so I blocked it.",
                f"I noticed your pattern and covered column {move}."
            ]))

    for col in board_obj.valid_moves():
        temp_board = copy_board(board_obj)
        temp_board.make_move(col, PLAYER)
        if temp_board.check_winner(PLAYER) and col == move:
            explanation.append(random.choice([
                f"I blocked your winning move in column {col}.",
                f"You were about to win in column {col}, so I stopped it.",
                f"That was a critical block in column {col}."
            ]))
            break

    if not explanation:
        explanation.append(random.choice([
            f"Column {move} looked good.",
            f"I liked the setup from that spot.",
            f"Just building pressure with that move."
        ]))

    # 🔊 Verbosity filtering
    if verbosity == "short":
        return explanation[0]
    elif verbosity == "long":
        return " Here's more: " + " ".join(explanation)
    else:  # medium
        return " ".join(explanation[:2]) if len(explanation) > 1 else explanation[0]
