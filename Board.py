'''
Module Name: Board.py
Purpose: store and manage square and board classes
Input(s): None
Output(s): None
Author(s):  Jacob Kice
            Joe Hotze
            Gunther Luechtefeld
Outside Source(s):  None
Creation Date: 10/22/2025
Updated Date: 11/07/2025
'''

import random as rng
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
        self.atk_by = False

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
        self.total_turns = 0
        self.powerup_delay_turns = 2
        self.powerup_chance = .75
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

    
    def _reset_atk_by(self):
        for rank in range(0,8):
            for file in range(0,8):
                self.board_array[rank][file].atk_by = False
    
    # used when the king is selected to determine ineligble spots for the king to move to
    def king_danger_spaces(self, color):
        self._reset_atk_by()
        coordinates = []

        # get all 'dangerous' coordinates
        for rank in range(0,8):
            for file in range(0,8):
                if self.board_array[rank][file].piece is not None and self.board_array[rank][file].piece.color is not color:
                    valid_moves = self.board_array[rank][file].piece.valid_moves(self)
                    for i in valid_moves:
                        self.board_array[rank][file].atk_by = True
                            
                    
        
    

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
        if type(player) is str:
            color = player
        else:
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
            elif piece_type == 'powerup':
                new_piece = Pieces.PowerUp(color, rank, file)
            else:
                raise(RuntimeError(f'Invalid Piece Type: {piece_type}'))
            
            self.board_array[rank][file].piece = new_piece
            #player.pieces.append(new_piece)
            return new_piece
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
            self.selected_moves = self.board_array[rank][file].piece.valid_moves(self)
            print(self.selected_moves)
        elif self.selected == (rank, file):
            self.selected = None
            self.selected_moves = None
        elif (rank, file) in self.selected_moves:
                self.move(rank, file)
                self.selected = None
                self.selected_moves = None

    def transform_pawn(self, piece):
        chance = rng.random()
        if chance > 0.9:
            #10% chance of becoming a queen
            new_type = 'queen'
        elif chance > 0.6:
            new_type = 'rook'
        elif chance > 0.3:
            new_type = 'bishop'
        else:
            new_type = 'knight'

        self.board_array[piece.rank][piece.file].piece = None

        return self.add_piece(piece.color, new_type, piece.rank, piece.file)

    def move(self, rank, file):
        '''
            Args:
                self
                rank: integer indicating the rank (row value) of the destination; valid values are 0 to 7
                file: integer indicating the file (column value) of the destination; valid values are 0 to 7
            Output:
                returns nothing
            Purpose:
                moves currently selected piece to new square and spawns powerups if applicable
            NOTE:
                needs integration of capture function once player objects are integrated
        '''
        bishop_conversion = False
        current_piece = self.board_array[self.selected[0]][self.selected[1]].piece # select piece to be moved
        if current_piece.character.lower() == 'b' and current_piece.has_powerup: # if the current piece is a powered up bishop
            # check if target is a piece of opposite color and is not a king
            if self.board_array[rank][file].piece is not None and self.board_array[rank][file].piece.color is not current_piece.color:  
                if self.board_array[rank][file].piece.character.lower() == 'k':
                    self.board_array[rank][file].piece.lives_left -= 1
                else:
                    if current_piece.color == 'white':
                        self.board_array[rank][file].piece.color = 'white'
                        self.board_array[rank][file].piece.character = self.board_array[rank][file].piece.character.lower()
                        bishop_conversion = True
                        current_piece.has_powerup = False

                    elif current_piece.color == 'black':
                        self.board_array[rank][file].piece.color = 'black'
                        self.board_array[rank][file].piece.character = self.board_array[rank][file].piece.character.capitalize()
                        bishop_conversion = True
                        current_piece.has_powerup = False


        if not bishop_conversion:
            if self.board_array[rank][file].piece is None or self.board_array[rank][file].piece.character.lower() != 'k':
                current_piece.rank, current_piece.file = rank, file # set current piece's location to new rank and file

                # knight power up handling
                if current_piece.character.lower() == 'n' and current_piece.has_powerup:
                    move_tuple = (self.selected[0] - rank, self.selected[1] - file)
                    if move_tuple not in [(-1,2), (1,2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2,1)]:
                        current_piece.has_powerup = False



                # rook power up handling
                if current_piece.character.lower() == 'r' and current_piece.has_powerup and self.board_array[rank][file].piece is not None:
                    explosion_targets = [(1, 0), (0, 1), (-1, 0), (0, -1)]
                    for target in explosion_targets:
                        target_rank, target_file = target
                        target_rank = target_rank + rank
                        target_file = target_file + file
                        # if target is in bounds and the square has a piece
                        if (target_rank >= 0 and target_rank < 8) and (target_file >= 0 and target_file < 8) and self.board_array[target_rank][target_file].piece is not None:
                            print(f"hit at {target_rank} {target_file}")
                            if self.board_array[target_rank][target_file].piece.character.lower() != 'k':
                                self.board_array[target_rank][target_file].piece = None
                            else:
                                self.board_array[target_rank][target_file].piece.lives_remaining -= 1

                            '''
                            # caution
                            # if uncommented, the rook will get power ups from pieces that it explodes, leading to irreversible damage to the game state
                            if self.board_array[target_rank][target_file].piece is not None and self.board_array[target_rank][target_file].piece.has_powerup:
                                current_piece.has_powerup = True
                            '''
                    
                    current_piece.has_powerup = False
                current_piece.has_powerup = False

                
                self.board_array[self.selected[0]][self.selected[1]].piece = None # set previous location to none

                # power up transfer
                if self.board_array[rank][file].piece is not None and self.board_array[rank][file].piece.has_powerup:
                    if current_piece.character.lower() == 'p':
                        #Call transform_pawn
                        current_piece = self.transform_pawn(current_piece)
                    elif current_piece.character.lower() == 'k':
                        current_piece.lives_remaining += 1
                    else:
                        current_piece.has_powerup = True

                # overwrite piece at destination
                self.board_array[rank][file].piece = current_piece

                # update has_moved for pawn and king
                if current_piece.character.lower() == "k" or current_piece.character.lower() == "p":
                    current_piece.has_moved = True

            else: # the captured piece is a king
                if self.board_array[rank][file].piece.lives_remaining > 1:
                    self.board_array[rank][file].piece.lives_remaining -= 1 # reduce lives by 1 if any remain
                else:
                    self.board_array[rank][file].piece = current_piece # capture if none remain
                    self.board_array[self.selected[0]][self.selected[1]].piece = None # set previous location to none

                current_piece.has_powerup = False
            

        

        # increment turn counter
        self.total_turns = self.total_turns + 1

        # powerup placement loop after a player moves
        # only happens after a specified amount of turns
        if self.total_turns > self.powerup_delay_turns and rng.random() <= self.powerup_chance:
            while True:
                rand_rank = rng.randint(0,7)
                rand_file = rng.randint(0,7)

                if self.board_array[rand_rank][rand_file].piece == None:
                    self.add_piece(self.player_one, 'powerup', rand_rank, rand_file)
                    break
                

            
        
    
if __name__ == '__main__':
    pass