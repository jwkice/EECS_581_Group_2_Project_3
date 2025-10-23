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

    def __str__(self):
        output = '   a  b  c  d  e  f  g  h\n'
        for index, row in enumerate(self.board_array):
            output += f'{index+1} '
            for cell in row:
                output += str(cell)
            output += '\n'
        return output

    
if __name__ == '__main__':
    game = Board()
    game.board_array[0][0].piece = Pieces.King('white')
    print(game)