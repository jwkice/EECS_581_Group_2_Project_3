from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import Board
import Pieces

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

games: Dict[str, Board.Board] = {}

class MoveRequest(BaseModel):
    game_id: str
    from_square: str # e.g. "e2"
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

class ValidMovesRequest(BaseModel):
    game_id: str
    square: str

class ValidMovesResponse(BaseModel):
    valid_moves: List[str]


# helper funcs
def position_to_indices(position: str) -> tuple:
    """ Convert chess notation ('e2') to array indices"""
    file = ord(position[0]) - ord('a') # 0-7
    rank = 8 - int(position[1]) # 0-7 inverted
    return (rank, file)

def indices_to_position(rank: int, file: int) -> str:
    """Convert array indicies to chess notation"""
    return f"{chr(file + ord('a'))}{8 - rank}"

def serialize_board(board: Board.Board) -> Dict[str, Optional[Dict]]:
    """Convert board state to JSON-serialized format"""
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
                    "has_powerup": square.piece.has_powerup
                }
            else:
                board_state[position] = None
    return board_state

def initialize_board(board: Board.Board):
    """Set up the initial chess position"""
    # Black pieces (rank 8)
    board.board_array[0][0].piece = Pieces.Rook('black')
    board.board_array[0][1].piece = Pieces.Knight('black')
    board.board_array[0][2].piece = Pieces.Bishop('black')
    board.board_array[0][3].piece = Pieces.Queen('black')
    board.board_array[0][4].piece = Pieces.King('black')
    board.board_array[0][5].piece = Pieces.Bishop('black')
    board.board_array[0][6].piece = Pieces.Knight('black')
    board.board_array[0][7].piece = Pieces.Rook('black')

    # Black pawns (rank 7)
    for i in range(8):
        board.board_array[1][i].piece = Pieces.Pawn('black')
    
    # White pawns (rank 2)
    for i in range(8):
        board.board_array[6][i].piece = Pieces.Pawn('white')
    
    # White pieces (rank 1)
    board.board_array[7][0].piece = Pieces.Rook('white')
    board.board_array[7][1].piece = Pieces.Knight('white')
    board.board_array[7][2].piece = Pieces.Bishop('white')
    board.board_array[7][3].piece = Pieces.Queen('white')
    board.board_array[7][4].piece = Pieces.King('white')
    board.board_array[7][5].piece = Pieces.Bishop('white')
    board.board_array[7][6].piece = Pieces.Knight('white')
    board.board_array[7][7].piece = Pieces.Rook('white')


# API endpoints
@app.get("/")
def read_root():
    return {"message": "Chess API is running"}

@app.post("/api/game/new", response_model=NewGameResponse)
def create_new_game():
    """Create a new chess game"""
    import uuid
    game_id = str(uuid.uuid4())
    
    board = Board.Board()
    initialize_board(board)
    games[game_id] = board
    
    return {
        "game_id": game_id,
        "board_state": serialize_board(board),
        "current_turn": board.players_turn
    }

@app.get("/api/game/{game_id}")
def get_game_state(game_id: str):
    """Get current state of a game"""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    board = games[game_id]
    return {
        "game_id": game_id,
        "board_state": serialize_board(board),
        "current_turn": board.players_turn,
        "game_over": board.game_over
    }

@app.post("/api/game/move", response_model=MoveResponse)
def make_move(move: MoveRequest):
    """Make a move on the board"""
    if move.game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    board = games[move.game_id]
    
    try:
        from_rank, from_file = position_to_indices(move.from_square)
        to_rank, to_file = position_to_indices(move.to_square)
        
        from_square = board.board_array[from_rank][from_file]
        to_square = board.board_array[to_rank][to_file]
        
        # Basic validation
        if from_square.piece is None:
            return {
                "success": False,
                "board_state": serialize_board(board),
                "current_turn": board.players_turn,
                "game_over": board.game_over,
                "message": "No piece at source square"
            }
        
        # Check if it's the correct player's turn
        piece_player = 1 if from_square.piece.color == 'white' else 2
        if piece_player != board.players_turn:
            return {
                "success": False,
                "board_state": serialize_board(board),
                "current_turn": board.players_turn,
                "game_over": board.game_over,
                "message": "Not your turn"
            }
        
        # Make move
        to_square.piece = from_square.piece
        from_square.piece = None
        
        # Switch turns
        board.players_turn = 2 if board.players_turn == 1 else 1
        
        return {
            "success": True,
            "board_state": serialize_board(board),
            "current_turn": board.players_turn,
            "game_over": board.game_over,
            "message": "Move successful"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/game/valid-moves", response_model=ValidMovesResponse)
def get_valid_moves(request: ValidMovesRequest):
    """Get valid moves for a piece at given position"""
    if request.game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    board = games[request.game_id]
    rank, file = position_to_indices(request.square)
    square = board.board_array[rank][file]
    
    if square.piece is None:
        return {"valid_moves": []}
    
    try:
        # Call valid_moves method when implemented
        valid_positions = square.piece.valid_moves(board, (rank, file))
        valid_squares = [indices_to_position(r, f) for r, f in valid_positions]
        return {"valid_moves": valid_squares}
    except NotImplementedError:
        # If not implemented yet, return empty list
        return {"valid_moves": []}
    
@app.delete("/api/game/{game_id}")
def delete_game(game_id: str):
    """Delete a game"""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    del games[game_id]
    return {"message": "Game deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)