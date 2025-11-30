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
            Gunther Luechtefeld
            Srihari Meyoor
Outside Source(s):  None
Creation Date: 10/22/2025
Updated Date: 11/25/2025
'''
# Idea: each piece is fed the board as well and uses that to broadcast its own valid moves
import Board as B # testing
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
        self.character = 'X'

    def valid_moves(self, board):
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
    
    def valid_power_moves(self, board):
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
        return self.character
    
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
    def __init__(self, color, rank, file):
        super().__init__(color, rank, file)
        if color == 'white':
            self.character = 'k'
        else:
            self.character = 'K'

        self.has_moved = False
        self.check = False
        self.checkmate = False
        self.lives_remaining = 3

    def valid_moves(self, board):
        valid_array = []
        friendly_pieces = []
        for rank_offset in range(-1, 2):
            for file_offset in range(-1, 2):
                new_rank = self.rank + rank_offset
                new_file = self.file + file_offset
                # if king's square is being attacked, king is in check
                if rank_offset == 0 and file_offset == 0: 
                    self.check = board.board_array[new_rank][new_file].atk_by

                if self._in_bounds(new_rank, new_file):
                    # valid move if enemy piece in range and not covered by enemy piece
                    if board.board_array[new_rank][new_file].piece is not None and board.board_array[new_rank][new_file].piece.color is not self.color:# and not board.board_array[new_rank][new_file].atk_by:
                        valid_array.append((new_rank, new_file))

                    # valid move if no piece on square and is not being covered by enemy piece
                    elif board.board_array[new_rank][new_file].piece is None and not board.board_array[new_rank][new_file].atk_by:
                        valid_array.append((new_rank, new_file))
        
        # no valid moves and king is in check
        if len(valid_array) == 0 and self.check:
            self.checkmate = True
            return valid_array

        else:
            self.checkmate = False
            return valid_array


class Queen(Piece):
    '''
        Purpose:
            extends Piece base class with movement rules specific to Queen piece
    '''
    def __init__(self, color, rank, file):
        super().__init__(color, rank, file)
        if color == 'white':
            self.character = 'q'
        else:
            self.character = 'Q'

    def valid_moves(self, board):
        powerup = self.has_powerup
        valid_array=[]
        directions_array = [(-1,-1), (-1,1), (1,1), (1, -1), (-1,0), (1,0), (0,-1), (0, 1)]
        for rank_offset, file_offset in directions_array:
            temp_rank = self.rank + rank_offset
            temp_file = self.file + file_offset
            while self._in_bounds(temp_rank, temp_file):
                if board.board_array[temp_rank][temp_file].piece is not None and board.board_array[temp_rank][temp_file].piece.color is not self.color:
                    #There is an opposition piece
                    valid_array.append((temp_rank, temp_file))
                    if self.has_powerup or board.board_array[temp_rank][temp_file].piece.color == 'green':
                        #If piece has powerup or target IS a power up, mark target square as a movement option, continue along the movement path
                        temp_rank += rank_offset
                        temp_file += file_offset
                        continue
                    else:
                        #Piece does not have powerup, mark target square as a movement option, terminate movement path
                        break
                
                # if there is a piece of same color
                elif board.board_array[temp_rank][temp_file].piece is not None:
                    if powerup:
                        #If piece has powerup, continue along the movement path
                        temp_rank += rank_offset
                        temp_file += file_offset
                        continue
                    else:
                        #Piece does not have powerup, terminate movement path
                        break

                valid_array.append((temp_rank, temp_file))
                temp_rank += rank_offset
                temp_file += file_offset

        return valid_array


class Knight(Piece):
    '''
        Purpose:
            extends Piece base class with movement rules specific to Knight piece
    '''
    def __init__(self, color, rank, file):
        super().__init__(color, rank, file)
        if color == 'white':
            self.character = 'n'
        else:
            self.character = 'N'

    def valid_moves(self, board):
        valid_array = []
        if self.has_powerup:
            knight_moves = [(-1,2), (1,2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2,1),
                            (0, 1), (1, 0), (0, -1), (-1, 0), (0, 2), (2, 0), (-2, 0), (0, -2)]

        else:
            knight_moves = [(-1,2), (1,2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2,1)]

        for potential_move in knight_moves:
            temp_rank = self.rank + potential_move[0]
            temp_file = self.file + potential_move[1]
            if self._in_bounds(temp_rank, temp_file):
                if board.board_array[temp_rank][temp_file].piece is not None and board.board_array[temp_rank][temp_file].piece.color is not self.color:
                    valid_array.append((temp_rank, temp_file))

                elif board.board_array[temp_rank][temp_file].piece is None:
                    valid_array.append((temp_rank, temp_file))
            
        return valid_array


class Bishop(Piece):
    '''
        Purpose:
            extends Piece base class with movement rules specific to Bishop piece
    '''
    def __init__(self, color, rank, file):
        super().__init__(color, rank, file)
        if color == 'white':
            self.character = 'b'
        else:
            self.character = 'B'

    def valid_moves(self, board):
        valid_array=[]
        directions_array = [(-1,-1), (-1,1), (1,1), (1, -1)]
        for rank_offset, file_offset in directions_array:
            temp_rank = self.rank + rank_offset
            temp_file = self.file + file_offset
            while self._in_bounds(temp_rank, temp_file):
                # if there is a piece and that piece is not self.color
                if board.board_array[temp_rank][temp_file].piece is not None and board.board_array[temp_rank][temp_file].piece.color is not self.color:
                    valid_array.append((temp_rank, temp_file))
                    if board.board_array[temp_rank][temp_file].piece.color != 'green':
                        break
                
                # if there is a piece of same color
                elif board.board_array[temp_rank][temp_file].piece and board.board_array[temp_rank][temp_file].piece.color == self.color:
                    break

                valid_array.append((temp_rank, temp_file))
                temp_rank += rank_offset
                temp_file += file_offset

        return valid_array


class Rook(Piece):
    '''
        Purpose:
            extends Piece base class with movement rules specific to Rook piece
    '''
    def __init__(self, color, rank, file):
        super().__init__(color, rank, file)
        if color == 'white':
            self.character = 'r'
        else:
            self.character = 'R'
            

    def valid_moves(self, board):
        valid_array=[]
        directions_array = [(-1,0), (1,0), (0,-1), (0, 1)]
        for rank_offset, file_offset in directions_array:
            
            temp_rank = self.rank + rank_offset
            temp_file = self.file + file_offset
            while self._in_bounds(temp_rank, temp_file):
                # if there is a piece and that piece is not self.color
                if board.board_array[temp_rank][temp_file].piece is not None and board.board_array[temp_rank][temp_file].piece.color is not self.color:
                    valid_array.append((temp_rank, temp_file))
                    if board.board_array[temp_rank][temp_file].piece.color != 'green':
                        break
                
                # if there is a piece of same color
                elif board.board_array[temp_rank][temp_file].piece is not None:
                    break

                valid_array.append((temp_rank, temp_file))
                temp_rank += rank_offset
                temp_file += file_offset

        return valid_array


class Pawn(Piece):
    '''
        Purpose:
            extends Piece base class with movement rules specific to Pawn piece
    '''
    def __init__(self, color, rank, file):
        super().__init__(color, rank, file)
        if color == 'white':
            self.character = 'p'
        else:
            self.character = 'P'

        self.has_moved = False
    
    def valid_moves(self, board):
        valid_array = []
        if self.color == 'white':
            
            if (self._in_bounds(self.rank - 1, self.file)) and (board.board_array[self.rank - 1][self.file].piece is None or board.board_array[self.rank - 1][self.file].piece.color == 'green'):
                valid_array.append((self.rank - 1, self.file))

            if (self._in_bounds(self.rank - 2, self.file)) and (board.board_array[self.rank - 1][self.file].piece is None or board.board_array[self.rank - 1][self.file].piece.color == 'green') and (board.board_array[self.rank - 2][self.file].piece is None or board.board_array[self.rank - 2][self.file].piece.color == 'green') and not self.has_moved:
                valid_array.append((self.rank - 2, self.file))
            
            if (self._in_bounds(self.rank - 1, self.file + 1)) and (board.board_array[self.rank - 1][self.file + 1].piece is not None and board.board_array[self.rank - 1][self.file + 1].piece.color != 'green'):
                if self.color is not board.board_array[self.rank - 1][self.file + 1].piece.color:
                    valid_array.append((self.rank - 1, self.file + 1))
            
            if (self._in_bounds(self.rank - 1, self.file - 1)) and (board.board_array[self.rank - 1][self.file - 1].piece is not None and board.board_array[self.rank - 1][self.file - 1].piece.color != 'green'):
                if self.color is not board.board_array[self.rank - 1][self.file - 1].piece.color:
                    valid_array.append((self.rank - 1, self.file - 1))
        

        elif self.color == 'black':
            if (self._in_bounds(self.rank + 1, self.file)) and (board.board_array[self.rank + 1][self.file].piece is None or board.board_array[self.rank + 1][self.file].piece.color == 'green'):
                valid_array.append((self.rank + 1, self.file))

            if (self._in_bounds(self.rank + 2, self.file)) and (board.board_array[self.rank + 1][self.file].piece is None or board.board_array[self.rank + 1][self.file].piece.color == 'green') and (board.board_array[self.rank + 2][self.file].piece is None or board.board_array[self.rank + 2][self.file].piece.color == 'green') and not self.has_moved:
                valid_array.append((self.rank + 2, self.file))
            
            if (self._in_bounds(self.rank + 1, self.file + 1)) and (board.board_array[self.rank + 1][self.file + 1].piece is not None and board.board_array[self.rank + 1][self.file + 1].piece.color != 'green'):
                if self.color is not board.board_array[self.rank + 1][self.file + 1].piece.color:
                    valid_array.append((self.rank + 1, self.file + 1))
            
            if (self._in_bounds(self.rank + 1, self.file - 1)) and (board.board_array[self.rank + 1][self.file - 1].piece is not None and board.board_array[self.rank + 1][self.file - 1].piece.color != 'green'):
                if self.color is not board.board_array[self.rank + 1][self.file - 1].piece.color:
                    valid_array.append((self.rank + 1, self.file - 1))

        return valid_array

class PowerUp(Piece):
    '''
        Purpose:
            extends Piece base class with a PowerUp that other pieces can pick up
    '''
    def __init__(self, color, rank, file):
        super().__init__(color, rank, file)
        self.character = 'A'
        self.color = 'green'
        self.has_powerup = True

    def valid_moves(self, board):
        return []


if __name__ == '__main__':
    # test_piece = Piece('white')
    # print(test_piece._in_bounds(-1, -1))
    game = B.Board()
    test_piece = PowerUp('white', 0, 0)
    print(test_piece.color)