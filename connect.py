import numpy as np
import random

class ConnectX:
    def __init__(self, rows=6, columns=7, win_length=4):
        self.rows = rows
        self.columns = columns
        self.win_length = win_length
        self.board = None
        self.current_player = 1
        self.done = False
        self.winner = None

    def reset(self):
        self.board = np.zeros((self.rows, self.columns), dtype=int)
        self.current_player = 1
        self.done = False
        self.winner = None
        return self.board

    def is_valid_move(self, column):
        return 0 <= column < self.columns and self.board[0, column] == 0

    def get_valid_moves(self):
        return [col for col in range(self.columns) if self.is_valid_move(col)]

    def drop_piece(self, column):
        if not self.is_valid_move(column):
            raise ValueError(f"Invalid move: Column {column}")
        for row in range(self.rows - 1, -1, -1):
            if self.board[row, column] == 0:
                self.board[row, column] = self.current_player
                if self.check_winner(row, column):
                    self.done = True
                    self.winner = self.current_player
                elif np.all(self.board != 0):
                    self.done = True  # It's a draw
                self.current_player = 3 - self.current_player  # Switch player
                return self.board
        return self.board

    def check_winner(self, row, column):
        def count_streak(dx, dy):
            streak = 0
            for step in range(1, self.win_length):
                r, c = row + step * dx, column + step * dy
                if 0 <= r < self.rows and 0 <= c < self.columns and self.board[r, c] == self.current_player:
                    streak += 1
                else:
                    break
            return streak

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            if count_streak(dx, dy) + count_streak(-dx, -dy) + 1 >= self.win_length:
                return True
        return False

def random_agent(board, valid_moves):
    return random.choice(valid_moves)

def rule_based_agent(board, valid_moves, game):
    # Check for winning move
    for move in valid_moves:
        temp_board = game.board.copy()
        game.drop_piece(move)
        if game.winner == game.current_player:
            game.board = temp_board  # Undo move
            return move
        game.board = temp_board  # Undo move

    # Block opponent's winning move
    opponent = 3 - game.current_player
    for move in valid_moves:
        temp_board = game.board.copy()
        game.board[temp_board == game.current_player] = opponent
        if game.check_winner(0, move):
            game.board = temp_board  # Undo move
            return move
        game.board = temp_board  # Undo move

    # Otherwise, play randomly
    return random_agent(board, valid_moves)

def play_game(agent1, agent2):
    game = ConnectX()
    game.reset()
    agents = {1: agent1, 2: agent2}
    while not game.done:
        valid_moves = game.get_valid_moves()
        agent = agents[game.current_player]
        move = agent(game.board, valid_moves, game) if agent == rule_based_agent else agent(game.board, valid_moves)
        game.drop_piece(move)
        print_board(game.board)
    if game.winner:
        print(f"Player {game.winner} wins!")
    else:
        print("It's a draw!")

def print_board(board):
    print("\n".join(["|".join(map(str, row)) for row in board]))
    print("-" * (board.shape[1] * 2 - 1))

if __name__ == "__main__":
    print("Welcome to ConnectX!")
    print("You can play as Player 1 against a random agent.")
    game = ConnectX()
    game.reset()
    while not game.done:
        print_board(game.board)
        if game.current_player == 1:
            valid_moves = game.get_valid_moves()
            move = int(input(f"Your turn! Choose a column {valid_moves}: "))
            while move not in valid_moves:
                print("Invalid move. Try again.")
                move = int(input(f"Your turn! Choose a column {valid_moves}: "))
        else:
            valid_moves = game.get_valid_moves()
            move = random_agent(game.board, valid_moves)
            print(f"Random agent plays: {move}")
        game.drop_piece(move)
    print_board(game.board)
    if game.winner:
        print(f"Player {game.winner} wins!")
    else:
        print("It's a draw!")
