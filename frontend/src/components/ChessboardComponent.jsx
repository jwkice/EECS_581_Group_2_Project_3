import React, { useState } from "react";
import { Chessboard } from "react-chessboard";

export default function ChessboardComponent() {
  const [highlightedSquares, setHighlightedSquares] = useState([]); // renamed from possibleMoves
  const [selectedCell, setSelectedCell] = useState(null); // fixed naming consistency

  const handleCellClick = (cell) => {
    if (selectedCell === cell) {
      setSelectedCell(null);
      setHighlightedSquares([]);
      return;
    }

    setSelectedCell(cell);

    // get all adjacent squares
    const adj = getAdjacentSquares(cell);
    setHighlightedSquares(adj);
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
      <h2>Chessboard Demo</h2>
      <Chessboard
        position="start"
        arePiecesDraggable={true}
        onSquareClick={handleCellClick}
      />
    </div>
  );
}

function getAdjacentSquares(cell) {
  const file = cell[0];
  const rank = parseInt(cell[1], 10);
  const files = "abcdefgh";
  const fileIndex = files.indexOf(file);
  const adjCells = [];

  for (let df = -1; df <= 1; df++) {
    for (let dr = -1; dr <= 1; dr++) {
      if (df === 0 && dr === 0) {
        continue
        };
      const newFileIndex = fileIndex + df;
      const newRank = rank + dr;
      if (newFileIndex >= 0 && newFileIndex < 8 && newRank >= 1 && newRank <= 8) {
        adjCells.push(files[newFileIndex] + newRank);
      }
    }
  }
  return adjCells;
}