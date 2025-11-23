from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from Board import Board
import Pieces

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active games in memory
games: Dict[str, Board] = {}

# Request/Response models
class MoveRequest(BaseModel):
    game_id: str
    from_square: str  # e.g., "e2"
    to_square: str

class NewGameResponse(BaseModel):
    game_id: str
    board_state: Dict[str, Optional[Dict]]
    current_turn: int

class MoveResponse(BaseModel):
    success: bool
    board_state: Dict[str, Optional[Dict]]
    current_turn: int
    game_over: bool
    message: Optional[str] = None
    captured_piece: Optional[str] = None

class ValidMovesRequest(BaseModel):
    game_id: str
    square: str

class ValidMovesResponse(BaseModel):
    valid_moves: List[str]

class GameStateResponse(BaseModel):
    game_id: str
    board_state: Dict[str, Optional[Dict]]
    current_turn: int
    game_over: bool
    current_player_color: str

# Helper functions
def position_to_indices(position: str) -> tuple:
    """Convert chess notation (ex. 'e2') to array indices"""
    file = ord(position[0]) - ord('a')  # 0-7
    rank = 8 - int(position[1])          # 0-7 inverted
    return (rank, file)

def indices_to_position(rank: int, file: int) -> str:
    """Convert array indices to chess notation"""
    return f"{chr(file + ord('a'))}{8 - rank}"

def serialize_board(board: Board) -> Dict[str, Optional[Dict]]:
    """Convert board state to JSON-serializable format"""
    board_state = {}
    for rank in range(8):
        for file in range(8):
            position = indices_to_position(rank, file)
            square = board.board_array[rank][file]
            if square.piece:
                piece_type = type(square.piece).__name__.lower()
                board_state[position] = {
                    "type": piece_type,
                    "color": square.piece.color,
                    "has_powerup": square.piece.has_powerup,
                    "character": square.piece.character
                }

                if piece_type == "king":
                    board_state[position]["lives_remaining"] = square.piece.lives_remaining

            else:
                board_state[position] = None
    return board_state

def get_current_player_color(board: Board) -> str:
    """Get the color of the current player"""
    return 'white' if board.players_turn == 1 else 'black'

# API endpoints
@app.get("/")
def read_root():
    return {"message": "Chess API is running", "version": "2.0"}

@app.post("/api/game/new", response_model=NewGameResponse)
def create_new_game():
    """Create a new chess game with initialized board"""
    import uuid
    game_id = str(uuid.uuid4())
    
    board = Board()
    games[game_id] = board
    
    return {
        "game_id": game_id,
        "board_state": serialize_board(board),
        "current_turn": board.players_turn
    }

@app.get("/api/game/{game_id}", response_model=GameStateResponse)
def get_game_state(game_id: str):
    """Get current state of a game"""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    board = games[game_id]
    return {
        "game_id": game_id,
        "board_state": serialize_board(board),
        "current_turn": board.players_turn,
        "game_over": board.game_over,
        "current_player_color": get_current_player_color(board)
    }

@app.post("/api/game/move", response_model=MoveResponse)
def make_move(move: MoveRequest):
    """Make a move on the board with validation"""
    if move.game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    board = games[move.game_id]
    
    try:
        from_rank, from_file = position_to_indices(move.from_square)
        to_rank, to_file = position_to_indices(move.to_square)
        
        from_square = board.board_array[from_rank][from_file]
        to_square = board.board_array[to_rank][to_file]
        
        # Validate piece exists
        if from_square.piece is None:
            return {
                "success": False,
                "board_state": serialize_board(board),
                "current_turn": board.players_turn,
                "game_over": board.game_over,
                "message": "No piece at source square"
            }
        
        # Check if it's the correct player's turn
        current_player_color = get_current_player_color(board)
        if from_square.piece.color != current_player_color:
            return {
                "success": False,
                "board_state": serialize_board(board),
                "current_turn": board.players_turn,
                "game_over": board.game_over,
                "message": f"Not your turn. It's {current_player_color}'s turn"
            }
        
        valid_moves = from_square.piece.valid_moves(board)
        
        # Check if the destination is valid move
        if (to_rank, to_file) not in valid_moves:
            return {
                "success": False,
                "board_state": serialize_board(board),
                "current_turn": board.players_turn,
                "game_over": board.game_over,
                "message": "Invalid move for this piece"
            }
        
        # Check for capture
        captured_piece = None
        if to_square.piece is not None:
            captured_piece = f"{to_square.piece.color} {type(to_square.piece).__name__}"
        
        # Set board's selected position for move() method
        board.selected = (from_rank, from_file)
        
        board.move(to_rank, to_file)
        
        # Switch turns
        board.players_turn = 2 if board.players_turn == 1 else 1
        
        # Check if the king is in check/checkmate
        opponent_color = get_current_player_color(board)
        board.king_danger_spaces(opponent_color)
        
        message = "Move successful"
        
        # Find opponent king and check if in check/checkmate
        for rank in range(8):
            for file in range(8):
                piece = board.board_array[rank][file].piece
                if piece and isinstance(piece, Pieces.King) and piece.color == opponent_color:
                    if piece.checkmate:
                        board.game_over = True
                        message = f"Checkmate! {current_player_color.capitalize()} wins!"
                    elif piece.check:
                        message = f"Check!"
                        if captured_piece:
                            message += f" {captured_piece} captured."
                    else:
                        if captured_piece:
                            message = f"{captured_piece} captured"
                    break
        else:
            # If no king found (shouldn't happen in normal game)
            if captured_piece:
                message = f"{captured_piece} captured"
        
        return {
            "success": True,
            "board_state": serialize_board(board),
            "current_turn": board.players_turn,
            "game_over": board.game_over,
            "message": message,
            "captured_piece": captured_piece
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error making move: {str(e)}")

@app.post("/api/game/valid-moves", response_model=ValidMovesResponse)
def get_valid_moves(request: ValidMovesRequest):
    """Get valid moves for a piece at given position"""
    if request.game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    board = games[request.game_id]
    
    try:
        rank, file = position_to_indices(request.square)
        square = board.board_array[rank][file]
        
        if square.piece is None:
            return {"valid_moves": []}
        
        # Get valid moves from the piece
        valid_positions = square.piece.valid_moves(board)
        valid_squares = [indices_to_position(r, f) for r, f in valid_positions]
        
        return {"valid_moves": valid_squares}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error getting valid moves: {str(e)}")

@app.delete("/api/game/{game_id}")
def delete_game(game_id: str):
    """Delete a game"""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    del games[game_id]
    return {"message": "Game deleted successfully"}

@app.get("/api/games")
def list_games():
    """List all active games"""
    return {
        "active_games": len(games),
        "game_ids": list(games.keys())
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)