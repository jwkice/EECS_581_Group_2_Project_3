import React, { useState, useEffect } from "react";
import "./Chessboard.css";
//white pieces
import whiteKing from "../assets/pieces-png/white-king.png";
import whiteQueen from "../assets/pieces-png/white-queen.png";
import whiteRook from "../assets/pieces-png/white-rook.png";
import whiteBishop from "../assets/pieces-png/white-bishop.png";
import whiteKnight from "../assets/pieces-png/white-knight.png";
import whitePawn from "../assets/pieces-png/white-pawn.png";
//black pieces
import blackKing from "../assets/pieces-png/black-king.png";
import blackQueen from "../assets/pieces-png/black-queen.png";
import blackRook from "../assets/pieces-png/black-rook.png";
import blackBishop from "../assets/pieces-png/black-bishop.png";
import blackKnight from "../assets/pieces-png/black-knight.png";
import blackPawn from "../assets/pieces-png/black-pawn.png";
import red_circle from "../assets/red_circle.png"

const API_URL = "http://localhost:8000";

const pieceImages = {
  white: {
    king: whiteKing,
    queen: whiteQueen,
    rook: whiteRook,
    bishop: whiteBishop,
    knight: whiteKnight,
    pawn: whitePawn,
  },
  black: {
    king: blackKing,
    queen: blackQueen,
    rook: blackRook,
    bishop: blackBishop,
    knight: blackKnight,
    pawn: blackPawn,
  }
};

export default function CustomBoard() {
  const [selected, setSelected] = useState(null);
  const [gameId, setGameId] = useState(null);
  const [boardState, setBoardState] = useState({});
  const [currentTurn, setCurrentTurn] = useState(1);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [validMoves, setValidMoves] = useState([]);
  
  const files = "abcdefgh";
  const ranks = [8,7,6,5,4,3,2,1];

  // Initialize new game on component mount
  useEffect(() => {
    createNewGame();
  }, []);

  const createNewGame = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/game/new`, {
        method: "POST",
      });
      const data = await response.json();
      setGameId(data.game_id);
      setBoardState(data.board_state);
      setCurrentTurn(data.current_turn);
      setMessage("New game started!");
    } catch (error) {
      console.error("Error creating game:", error);
      setMessage("Failed to create game");
    }
    setLoading(false);
  };

  const handleGridClick = async (square) => {
    if (loading || !gameId) return;

    // Select a piece
    if (!selected && boardState[square]) {
      setSelected(square);
      setMessage(`Selected ${square}`);

      //check for valid moves
      const response = await fetch(`${API_URL}/api/game/valid-moves`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            game_id: gameId,
            square: square
          })
        }
      );
      
      const data = await response.json();
      setValidMoves(data.valid_moves || []);

    }
    // Make a move
    else if (selected) {
      if(selected === square) {
        setSelected(null);
        setValidMoves([]);
        return;
      }
      setLoading(true);
      try {
        const response = await fetch(`${API_URL}/api/game/move`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            game_id: gameId,
            from_square: selected,
            to_square: square,
          }),
        });
        
        const data = await response.json();

        if (data.success) {
          setBoardState(data.board_state);
          setCurrentTurn(data.current_turn);
          setValidMoves([]);
          setMessage(data.message || "Move successful");
        } else {
          setMessage(data.message || "Invalid move");
        }
      } catch (error) {
        console.error("Error making move:", error);
        setMessage("Failed to make move");
      }
      setSelected(null);
      setLoading(false);
    }
  };

  const getPieceImage = (pieceData) => {
    if (!pieceData) return null;
    return pieceImages[pieceData.color]?.[pieceData.type];
  };

  return (
    <div style={{ padding: "20px", maxWidth: "600px", margin: "0 auto" }}>
      <div style={{ marginBottom: "20px", textAlign: "center" }}>
        <h2>Chess Game</h2>
        <p>Turn: {currentTurn === 1 ? "White" : "Black"}</p>
        <p style={{ color: message.includes("Failed") ? "red" : "green" }}>
          {message}
        </p>
        <button 
          onClick={createNewGame}
          disabled={loading}
          style={{
            padding: "10px 20px",
            fontSize: "16px",
            cursor: loading ? "not-allowed" : "pointer",
            backgroundColor: "#4CAF50",
            color: "white",
            border: "none",
            borderRadius: "5px",
          }}
        >
          New Game
        </button>
      </div>

      <div className="board">
        {ranks.map((rank) => (
          <div key={rank} className="rank">
            {files.split("").map((file, fileIdx) => {
              const square = `${file}${rank}`;
              const isDark = (fileIdx + rank) % 2 === 1;
              const color = isDark ? "#ABE7B2" : "#ECF4E8";
              const isSelected = selected === square;
              const pieceData = boardState[square];
              const isValidMove = validMoves.includes(square);

              return (
                <div
                  key={square}
                  className="square"
                  style={{
                    backgroundColor: isSelected ? "#FFD700" : color,
                    cursor: loading ? "not-allowed" : "pointer",
                    opacity: loading ? 0.6 : 1,
                  }}
                  onClick={() => handleGridClick(square)}
                >
                  {pieceData && (
                    <img 
                      src={getPieceImage(pieceData)} 
                      alt={`${pieceData.color} ${pieceData.type}`}
                      className="piece" 
                    />
                  )}
                  {isValidMove && (
                    <img
                      src={red_circle}
                      height="35px"
                      width="35px"
                      className={"validmove"}/>
                  )}
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
}