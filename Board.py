import Pieces

class Square():
    def __init__(self):
        self.piece = None
        self.powerup = False

    def __str__(self):
        if self.piece is None:
            return '[ ]'
        else:
            return f'[{str(self.piece)}]'

class Board():
    def __init__(self):
        self.board_array = [[Square() for _ in range(8)] for _ in range(8)]
        self.game_over = False
        self.players_turn = 1
        self.selected = None
        self.selected_moves = None

    def __str__(self):
        output = ''
        for index, row in enumerate(self.board_array):
            output += f'{8-index} '
            for cell in row:
                output += str(cell)
            output += '\n'
        
        output += '   a  b  c  d  e  f  g  h\n'
        return output

    def add_piece(self, piece_type, color, rank, file):
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
    game.add_piece('king', 'white', 4, 4)
    print(game)
    game.select(4, 4)
    rank = int(input('Rank: '))
    file = int(input('File: '))
    game.select(rank, file)
    print(game)
    game.select(rank, file)