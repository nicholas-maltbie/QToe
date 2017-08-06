"""

Contains definition for a Tic Tac Toe game.

"""

class TicTacToe:
    
    def __init__(self, size = 3):
        """Returns a tic tac toe game"""
        self.board = [0] * size * size
        self.size = size
    
    def get_piece(self, row, col):
        """Gets a piece at a specified row and column"""
        assert row < self.size and col < self.size
        return self.board[row * self.size + col]

