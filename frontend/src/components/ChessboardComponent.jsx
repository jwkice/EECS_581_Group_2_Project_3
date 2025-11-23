import React, { useState, useEffect } from "react";
import "./Chessboard.css";

import whiteKing from "../assets/pieces-png/kw.svg";
import whiteQueen from "../assets/pieces-png/qw.svg";
import whiteRook from "../assets/pieces-png/rw.svg";
import whiteBishop from "../assets/pieces-png/bw.svg";
import whiteKnight from "../assets/pieces-png/nw.svg";
import whitePawn from "../assets/pieces-png/pw.svg";

import blackKing from "../assets/pieces-png/kb.svg";
import blackQueen from "../assets/pieces-png/qb.svg";
import blackRook from "../assets/pieces-png/rb.svg";
import blackBishop from "../assets/pieces-png/bb.svg";
import blackKnight from "../assets/pieces-png/nb.svg";
import blackPawn from "../assets/pieces-png/pb.svg";

import red_circle from "../assets/red_circle.png"
import powerup from "../assets/pieces-png/powerup.gif"

import slashGif from "../assets/pieces-png/jinn_duel.gif";

import flame from "../assets/pieces-png/flame.gif";

import heart from "../assets/pieces-png/heart.png"



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
  },
};

export default function CustomBoard() {
  const [selected, setSelected] = useState(null);
  const [gameId, setGameId] = useState(null);
  const [boardState, setBoardState] = useState({});
  const [currentTurn, setCurrentTurn] = useState(1);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [validMoves, setValidMoves] = useState([]);
  const [showKillBanner, setShowKillBanner] = useState(false);
  const [whiteLives, setWhiteLives] = useState(1);
  const [blackLives, setBlackLives] = useState(1);



  
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

      let wLives = 0;
          let bLives = 0;

          Object.values(data.board_state).forEach(square => {
              if (!square) return;

              if (square.type === "king") {
                  if (square.color === "white") wLives = square.lives_remaining;
                  if (square.color === "black") bLives = square.lives_remaining;
              }
          });

          setWhiteLives(wLives);
          setBlackLives(bLives);

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

        console.log(data);

        if (data.success) {
          setBoardState(data.board_state);

          let wLives = 0;
          let bLives = 0;

          Object.values(data.board_state).forEach(square => {
              if (!square) return;

              if (square.type === "king") {
                  if (square.color === "white") wLives = square.lives_remaining;
                  if (square.color === "black") bLives = square.lives_remaining;
              }
          });

          setWhiteLives(wLives);
          setBlackLives(bLives);

          setCurrentTurn(data.current_turn);

          if (data.captured_piece && data.captured_piece !== "green? whatever it doesnt really matter PowerUp") {
            setShowKillBanner(true);

            setTimeout(() => {
                setShowKillBanner(false);
            }, 1600);
        }

          setMessage(data.message || "Move successful");
        

          setValidMoves([]);
          console.log(data);

        }
        
        else {
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
    <div className="page-container">
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

      <div className="lives-header">
        <div className="lives-left">
          <span className="lives-label">White Lives: </span>
          {[...Array(whiteLives)].map((_, i) => (
            <img key={i} src={heart} className="heart-icon" />
          ))}
        </div>

        <div className="lives-right">
          <span className="lives-label">Black Lives: </span>
          {[...Array(blackLives)].map((_, i) => (
            <img key={i} src={heart} className="heart-icon" />
          ))}
        </div>
      </div>

      <div className="board-wrapper">
  
      {showKillBanner && (
        <div className="kill-banner">
          <img src={slashGif} alt="Kill Animation" />
        </div>
      )}
      <div className="board-frame">
      <div className="board">
        {ranks.map((rank) => (
          <div key={rank} className="rank">
            {files.split("").map((file, fileIdx) => {
              const square = `${file}${rank}`;
              const isDark = (fileIdx + rank) % 2 === 1;
              const color = isDark ? "#8CA9FF" : "#8CE4FF";
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
                  {pieceData && pieceData.type !== "powerup" && !pieceData.has_powerup && (
                    <img 
                      src={getPieceImage(pieceData)} 
                      alt={`${pieceData.color} ${pieceData.type}`}
                      className="piece" 
                    />
                  )}

                  {pieceData && pieceData.type !== "powerup" && pieceData.has_powerup && (
                    <div className="piece-wrapper">
                      <img 
                        src={getPieceImage(pieceData)}
                        alt={`${pieceData.color} ${pieceData.type}`}
                        className="piece"
                      />
                      <img 
                        src={flame}
                        alt="Super Saiyan Power"
                        className="ssj-overlay"
                      />
                    </div>
                  )}


                  {pieceData?.type === "powerup" && (
                    <img 
                        src={powerup}
                        alt="Powerup"
                        className="powerup-spin"
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
    </div>
    </div>
  );
}