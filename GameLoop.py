from Player import Player
from Board import Board
import Pieces

def translate_input(rank_file): # translates readable input into the abomination we have going on
    rank = rank_file[1]
    file = rank_file[0]
    file_index = ord(file) - ord('a') # this gets the ascii code, so a-h returns 1-8
    rank_index = 8 - int(rank)
    return (rank_index, file_index)

def main():
    current_game = Board()
    print("Begininng Game. Move format: position of piece to be moved, new position. Ex: e2 e4\n")

    while current_game.game_over != True:
        print(current_game)

        if current_game.players_turn == 1:
            current_player = current_game.player_one # white 
        else:
            current_player = current_game.player_two # black 
        
        print(f"{current_player.color}'s turn.")

        move_input = input("Enter your move (type quit to quit): ").lower()
        if move_input == ("quit"):
            print("Ending game.")
            break


        try:
            source_rawinput, dest_rawinput = move_input.split()
            source = translate_input(source_rawinput)
            dest = translate_input(dest_rawinput)

        except Exception:
            print("Invalid move input. Please try again.")
            continue


        source_square = current_game.board_array[source[0]][source[1]]
        if source_square.piece == None:
            print("No piece at that position.")
            continue
        if source_square.piece.color != current_player.color:
            print(f"That's not your piece. ({current_player.color}'s turn)")
            continue

        current_game.selected = source
        valid_moves = source_square.piece.valid_moves(current_game)
        if dest not in valid_moves:
            print("Invalid move for that piece.")
            current_game.selected = None
            continue

        dest_square = current_game.board_array[dest[0]][dest[1]]
        if dest_square.piece is not None:
            print(f"{current_player.color.capitalize()} captures {dest_square.piece.character}!")
            print(current_game.board_array[dest[0]][dest[1]].piece.has_powerup)

        current_game.move(dest[0], dest[1])

        if current_game.players_turn == 1:
            current_game.players_turn = 2
        else:
            current_game.players_turn = 1
    
    print("Game over.")

if __name__ == "__main__":
    main()