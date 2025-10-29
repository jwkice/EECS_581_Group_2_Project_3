'''
Module Name: Pieces.py
Purpose: store and manage piece base class and specific derived classes
Contents:   Piece class
            King class
            Queen class
            Knight class
            Bishop class
            Rook class
            Pawn class
Input(s): None
Output(s): None
Author(s):  Jacob Kice
            Joe Hotze
Outside Source(s):  None
Creation Date: 10/22/2025
Updated Date: 10/28/2025
'''

class Piece():
    '''
        Args:
            color: string indicating which player the piece belongs to; valid values: 'white', 'black'
            rank: integer indicating the rank (row value) of the piece; valid values are 0 to 7
            file: integer indicating the file (column value) of the piece; valid values are 0 to 7
        Purpose:
            base class for chess pieces
            initalizes class members, generic and shared methods
    '''
    def __init__(self, color, rank, file):
        self.color = color
        self.rank = rank
        self.file = file
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
    '''
        Purpose:
            extends Piece base class with movement rules specific to King piece
    '''
    def valid_moves(self, board):
        valid_array = []
        for rank_offset in range(-1, 2):
            for file_offset in range(-1, 2):
                if rank_offset == 0 and file_offset == 0:
                    continue

                if self._in_bounds(self.rank+rank_offset, self.file+file_offset):
                    valid_array.append((self.rank+rank_offset, self.file+file_offset))
                
        return valid_array

class Queen(Piece):
    '''
        Purpose:
            extends Piece base class with movement rules specific to Queen piece
    '''
    def valid_moves(self, board):
        valid_array=[]
        directions_array = [(-1,-1), (-1,1), (1,1), (1, -1), (-1,0), (1,0), (0,-1), (0, 1)]
        for rank_offset, file_offset in directions_array:
            temp_rank = self.rank + rank_offset
            temp_file = self.file + file_offset
            while self._in_bounds(temp_rank, temp_file):
                valid_array.append((temp_rank, temp_file))
                temp_rank += rank_offset
                temp_file += file_offset

        return valid_array

class Knight(Piece):
    '''
        Purpose:
            extends Piece base class with movement rules specific to Knight piece
    '''
    pass

class Bishop(Piece):
    '''
        Purpose:
            extends Piece base class with movement rules specific to Bishop piece
    '''
    def valid_moves(self, board):
        valid_array=[]
        directions_array = [(-1,-1), (-1,1), (1,1), (1, -1)]
        for rank_offset, file_offset in directions_array:
            temp_rank = self.rank + rank_offset
            temp_file = self.file + file_offset
            while self._in_bounds(temp_rank, temp_file):
                valid_array.append((temp_rank, temp_file))
                temp_rank += rank_offset
                temp_file += file_offset

        return valid_array

class Rook(Piece):
    '''
        Purpose:
            extends Piece base class with movement rules specific to Rook piece
    '''
    def valid_moves(self, board):
        valid_array=[]
        directions_array = [(-1,0), (1,0), (0,-1), (0, 1)]
        for rank_offset, file_offset in directions_array:
            temp_rank = self.rank + rank_offset
            temp_file = self.file + file_offset
            while self._in_bounds(temp_rank, temp_file):
                valid_array.append((temp_rank, temp_file))
                temp_rank += rank_offset
                temp_file += file_offset

        return valid_array


class Pawn(Piece):
    '''
        Purpose:
            extends Piece base class with movement rules specific to Pawn piece
    '''
    pass


if __name__ == '__main__':
    test_piece = Piece('white')
    print(test_piece._in_bounds(-1, -1))