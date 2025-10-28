class Piece():
    def __init__(self, color):
        self.color = color
        self.has_powerup = False

    def valid_moves(self, board, position):
        '''
            Args:
                board: current game state
                position: current position of game piece (NOTE: may get replaced with position member within the class)
            Output:
                returns array of valid moves the piece can make on the current board
            Purpose:
                determines all possible moves that can be made by the current piece on the current board
        '''
        raise(NotImplementedError('valid_moves has not been implemented for the calling object'))
    
    def valid_power_moves(self, board, position):
        '''
            Args:
                board: current game state
                position: current position of game piece (NOTE: may get replaced with position member within the class)
            Output:
                returns array of valid moves the piece can make with its powerup on the current board
            Purpose:
                determines all possible moves that can be made by the current piece with its powerup on the current board
        '''
        raise(NotImplementedError('valid_power_moves has not been implemented for the calling object'))
    
    def __str__(self):
        '''
            Args:
                self
            Output:
                string representation of piece
            Purpose:
                formats the piece object as a string for display purposes
        '''
        return 'X'
    
    def _in_bounds(self, x, y):
        '''
            Args:
                self
                x: integer indicating X coordinate of square to check
                y: integer indicating Y coordinate of square to check
            Output:
                returns boolean value
            Purpose:
                determines if provided X and Y coordinates refer to a grid square within the bounds of the game board
        '''
        return (x >= 0 and x < 8) and (y >= 0 and y < 8)
    
class King(Piece):
    pass

class Queen(Piece):
    pass

class Knight(Piece):
    pass

class Bishop(Piece):
    pass

class Rook(Piece):
    pass

class Pawn(Piece):
    pass


if __name__ == '__main__':
    test_piece = Piece('white')
    print(test_piece._in_bounds(-1, -1))