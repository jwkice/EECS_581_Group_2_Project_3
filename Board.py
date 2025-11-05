'''
Module Name: Board.py
Purpose: store and manage square and board classes
Input(s): None
Output(s): None
Author(s):  Jacob Kice
            Joe Hotze
Outside Source(s):  None
Creation Date: 10/22/2025
Updated Date: 10/28/2025
'''

import Pieces
from Player import Player

class Square():
    '''
        Args:
            None
        Purpose:
            serves as manager for individual square on game board
            stores square's piece and powerup status
    '''
    def __init__(self):
        self.piece = None
        self.powerup = False

    def __str__(self):
        '''
            Args:
                self
            Output:
                string representation of grid square
            Purpose:
                formats the square object as a string for display purposes
        '''
        if self.piece is None:
            return '[ ]'
        else:
            return f'[{str(self.piece)}]'

class Board():
    '''
        Args:
            None
        Purpose: 
            serves as a game board manager for power chess
            stores game board and game state information
            handles direct interactions with game board
    '''
    def __init__(self):
        self.board_array = [[Square() for _ in range(8)] for _ in range(8)]
        self.game_over = False
        self.players_turn = 1
        self.selected = None
        self.selected_moves = None
        self._initialize()

    def _initialize(self):
        '''
            Args:
                self
            Output:
                None
            Purpose:
                initializes player and piece objects
                assign created pieces to appropriate player object, and board position
                sets player 1 as current player
        '''
        self.player_one = Player('white')
        self.player_one.turn = True
        self.player_two = Player('black')

        for i in range(16): #Place pawns
            if i < 8:   #Place white pawns
                self.add_piece(self.player_one, 'pawn', 6, i)
            else:   #Place black pawns
                self.add_piece(self.player_two, 'pawn', 1, i-8)

        #Place rooks
        self.add_piece(self.player_one, 'rook', 7, 0)
        self.add_piece(self.player_one, 'rook', 7, 7)
        self.add_piece(self.player_two, 'rook', 0, 0)
        self.add_piece(self.player_two, 'rook', 0, 7)

        #Place knights
        self.add_piece(self.player_one, 'knight', 7, 1)
        self.add_piece(self.player_one, 'knight', 7, 6)
        self.add_piece(self.player_two, 'knight', 0, 1)
        self.add_piece(self.player_two, 'knight', 0, 6)

        #Place bishops
        self.add_piece(self.player_one, 'bishop', 7, 2)
        self.add_piece(self.player_one, 'bishop', 7, 5)
        self.add_piece(self.player_two, 'bishop', 0, 2)
        self.add_piece(self.player_two, 'bishop', 0, 5)

        #Place queens
        self.add_piece(self.player_one, 'queen', 7, 3)
        self.add_piece(self.player_two, 'queen', 0, 3)

        #Place kings
        self.add_piece(self.player_one, 'king', 7, 4)
        self.add_piece(self.player_two, 'king', 0, 4)        

    def __str__(self):
        '''
            Args:
                self
            Output:
                string representation of board
            Purpose:
                formats the board object as a string for display purposes
        '''
        output = ''
        for index, row in enumerate(self.board_array):
            output += f'{8-index} '
            for cell in row:
                output += str(cell)
            output += '\n'
        
        output += '   a  b  c  d  e  f  g  h\n'
        return output

    def add_piece(self, player, piece_type, rank, file):
        '''
            Args:
                self
                piece_type: string indicating type of piece to create; valid values are 'pawn', 'knight', 'bishop', 'rook', 'queen', 'king'
                color: string indicating which player the piece belongs to; valid values are 'white' and 'black'
                rank: integer indicating the rank (row value) of the new piece; valid values are 0 to 7
                file: integer indicating the file (column value) of the new piece; valid values are 0 to 7
            Output:
                returns nothing
            Purpose:
                initializes a new piece of the indicated type, assigns it to the given square on the board
        '''
        color = player.color
        if self.board_array[rank][file].piece is None:
            if piece_type == 'pawn':
                new_piece = Pieces.Pawn(color, rank, file)
            elif piece_type == 'knight':
                new_piece = Pieces.Knight(color, rank, file)
            elif piece_type == 'bishop':
                new_piece = Pieces.Bishop(color, rank, file)
            elif piece_type == 'rook':
                new_piece = Pieces.Rook(color, rank, file)
            elif piece_type == 'queen':
                new_piece = Pieces.Queen(color, rank, file)
            elif piece_type == 'king':
                new_piece = Pieces.King(color, rank, file)
            else:
                raise(RuntimeError(f'Invalid Piece Type: {piece_type}'))
            
            self.board_array[rank][file].piece = new_piece
            player.pieces.append(new_piece)
        else:
            raise(RuntimeError(f'Square ({rank}, {file}) already has a piece'))
    
    def select(self, rank, file):
        '''
            Args:
                self
                rank: integer indicating the rank (row value) of the selected piece; valid values are 0 to 7
                file: integer indicating the file (column value) of the selected piece; valid values are 0 to 7
            Output:
                returns nothing
            Purpose:
                handles selection of board square
                    if new selection, obtains and displays valid moves of current piece
                    if same as currently selected, unselects that square
                    if in list of valid moves, calls move function and clears selection
            NOTE:
                needs integration with player objects
                needs checking for invalid selections if not handled by interface
        '''
        if self.selected is None:
            self.selected = (rank, file)
            self.selected_moves = self.board_array[rank][file].piece.valid_moves(self.board_array)
            print(self.selected_moves)
        elif self.selected == (rank, file):
            self.selected = None
            self.selected_moves = None
        elif (rank, file) in self.selected_moves:
                self.move(rank, file)
                self.selected = None
                self.selected_moves = None

    def move(self, rank, file):
        '''
            Args:
                self
                rank: integer indicating the rank (row value) of the destination; valid values are 0 to 7
                file: integer indicating the file (column value) of the destination; valid values are 0 to 7
            Output:
                returns nothing
            Purpose:
                moves currently selected piece to new square
            NOTE:
                needs integration of capture function once player objects are integrated
        '''
        current_piece = self.board_array[self.selected[0]][self.selected[1]].piece
        current_piece.rank, current_piece.file = rank, file
        self.board_array[self.selected[0]][self.selected[1]].piece = None
        self.board_array[rank][file].piece = current_piece

            
        
    
if __name__ == '__main__':
    game = Board()
    print(game)