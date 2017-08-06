"""

Contains definition for a Tic Tac Toe game.

"""

import numpy as np
import random
import sys

class TicTacToe:
    """Definition for a game of tic tac toe"""
    
    #Static functions and features
    
    def make_move(player, row, col):
        """Makes a move for a given player at a row and column"""
        return {'player':player, 'row':row, 'col':col}
        
    #Empty space
    empty = '_'
    
    tie = 'Tie'
    
    #Bounded functions
    
    def __init__(self, size = 3):
        """Returns a tic tac toe game"""
        self.board = [self.empty] * size * size
        self.size = size
    
    def reset_board(self):
        """Resets the game board"""
        self.board = [self.empty] * self.size * self.size
    
    def get_piece(self, row, col):
        """Gets a piece at a specified row and column"""
        assert row < self.size and col < self.size
        return self.board[row * self.size + col]
    
    def is_empty(self, row, col):
        """Checks if a given location is empty"""
        return self.get_piece(row, col) == self.empty
    
    def set_piece(self, row, col, player):
        """Sets a piece at a given row and column"""
        assert row < self.size and col < self.size
        self.board[row * self.size + col] = player
    
    def get_board_vector(self, fn = lambda x: x):
        """Gets the board as a numpy vector"""
        return np.array([fn(i) for i in self.board])
        
    def is_valid(self, move):
        """Checks if a move is valid"""
        return self.is_empty(move['row'], move['col'])
     
    def apply_move(self, move):
        """Applys a move to this game's board"""
        self.set_piece(move['row'], move['col'], move['player'])
    
    def has_won(self):
        """Checks if a player has won, and if so, returns the player. If no 
        player has won, then returns None. If the game is tied, it will 
        return 'Tie' """
        def all_equal(values):
            """Checkes if all the elements in a list are equal"""
            if len(values) == 0:
                return True
            v_0 = values[0]
            for value in values[1:]:
                if value != v_0:
                    return False
            return True
        piece_sets = []
        #Check for horiz win
        piece_sets.extend([[self.get_piece(row, col) for col in range(self.size)]
                            for row in range(self.size)])
        #Check for vertial win
        piece_sets.extend([[self.get_piece(row, col) for row in range(self.size)]
                            for col in range(self.size)])
        #Check for diagonal win
        piece_sets.append([self.get_piece(i,i) for i in range(self.size)])
        piece_sets.append([self.get_piece(self.size - i - 1,i) for i in range(self.size)])
        
        #Check victory
        for set in piece_sets:
            if set[0] != self.empty and all_equal(set):
                return set[0]
        #Check tie
        all_full = True
        for row in range(self.size):
            for col in range(self.size):
                if self.is_empty(row, col):
                    all_full = False
        if all_full:
            return self.tie
        #If no victory, return false
        return None
        
    def print_board(self):
        """Prints a borad to the console"""
        for row in range(self.size):
            print(" ".join([self.get_piece(row, col) for col in range(self.size)]))
        print()
    
    def play_game(self, player_1, player_2, 
        player_1_piece = 'x', player_2_piece = 'y', 
        random_start = True, log = True):
        """Plays a game with two players, each 'player' is a definition for a 
        function that when passed a board and player piece as arguments will 
        return a move made using make_move.
        
        This game will return the winning player or 'Tie' if the game ends 
        in a tie."""
        #First reset the board
        self.reset_board()
        
        players = [player_1, player_2]
        pieces = [player_1_piece, player_2_piece]
        curr = (0 if not random_start else random.randrange(len(players)))
        
        other = lambda player: (player + 1) % len(players)
        
        #Play until a player has won or it's a tied game
        ended = None
        while not ended:
            move = players[curr](self, pieces[curr])
            
            if not self.is_valid(move):
                print(move)
                return other(curr)
            
            self.apply_move(move)
            
            curr = other(curr)
            
            if log:
                self.print_board()
                
            ended = self.has_won()
        
        return ended

if __name__ == "__main__":
    #Play test game of tic tac toe
    
    def random_player(board, player):
        sel = random.choice([(row, col) for row in range(board.size) 
                                        for col in range(board.size)
                             if board.is_empty(row, col)])
        
        return TicTacToe.make_move(player, sel[0], sel[1])
    
    def human_player(board, player):
        board.print_board()
        print('Type \'q\' to quit')
        print('You are "' + player + '"')
        print('Type location of play as \'row col\'')
        print('(Rows and columns start at 1)')
        row = -1
        col = -1
        attempts = 0
        while row < 1 or row > board.size + 1 or \
              col < 1 or col > board.size + 1 or \
              not board.is_empty(row, col):
            if attempts > 0:
                print('That is not a valid move, look at the board again')
                board.print_board()
            try:
                val = input()
                row, col = (int(elem) - 1 for elem in val.strip().split(' '))
            except:
                if val.lower().strip() == 'q':
                    sys.exit()
            attempts += 1
        return TicTacToe.make_move(player, row, col)
    
    print('playing game')
    
    game = TicTacToe()
    print(game.play_game(random_player, human_player), "has won the game")
