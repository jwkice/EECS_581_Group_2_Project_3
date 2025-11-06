import React, { useState } from "react";
import "./Chessboard.css"; // add CSS for layout
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

export default function CustomBoard() {
  const [selected, setSelected] = useState(null);
  const files = "abcdefgh";
  const ranks = [8,7,6,5,4,3,2,1];

  const handleGridClick = async (square) => {
    if(!selected && pieces[square]){
      setSelected(square);
    }
    
    else if (selected){
      const from = selected;
      const to = square;
      const movedPiece = pieces[from];
      const newPieces = { ...pieces, [to]: movedPiece, [from]: undefined };
      setPieces(newPieces);

      setSelected(null);
    }
  };

  const [pieces, setPieces] = useState({
    a8: blackRook, b8: blackKnight, c8: blackBishop, d8: blackQueen,
    e8: blackKing, f8: blackBishop, g8: blackKnight, h8: blackRook,
    a7: blackPawn, b7: blackPawn, c7: blackPawn, d7: blackPawn,
    e7: blackPawn, f7: blackPawn, g7: blackPawn, h7: blackPawn,

    a2: whitePawn, b2: whitePawn, c2: whitePawn, d2: whitePawn,
    e2: whitePawn, f2: whitePawn, g2: whitePawn, h2: whitePawn,
    a1: whiteRook, b1: whiteKnight, c1: whiteBishop, d1: whiteQueen,
    e1: whiteKing, f1: whiteBishop, g1: whiteKnight, h1: whiteRook,
  });
  return (
    <div className="board">
      {ranks.map((rank) => (
        <div key={rank} className="rank">
          {files.split("").map((file, fileIdx) => {
            const square = `${file}${rank}`;
            const isDark = (fileIdx + rank) % 2 === 1;
            const color = isDark ? "#ABE7B2" : "#ECF4E8";
            const isSelected = selected === square;

            return (
              <div
                key={square}
                className="square"
                style={{
                  backgroundColor: isSelected ? "#FFD700" : color,
                }}
                onClick={() => handleGridClick(square)}
              >
                {pieces[square] && (
                  <img src={pieces[square]} alt={square} className="piece" />
                )}
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
}