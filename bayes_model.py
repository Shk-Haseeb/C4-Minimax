from board import COLUMNS

class PlayerModel:
    def __init__(self):
        self.column_counts = [1 for _ in range(COLUMNS)] 
        self.total_moves = COLUMNS 

    def record_move(self, col):
        self.column_counts[col] += 1
        self.total_moves += 1

    def predict_column_probabilities(self):
        return [count / self.total_moves for count in self.column_counts]

    def most_likely_column(self):
        return self.column_counts.index(max(self.column_counts))
