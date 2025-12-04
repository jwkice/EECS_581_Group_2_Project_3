### For Development

Group 3 Project Video:
https://drive.google.com/file/d/1Z-j8uH76jGFo-N-2eG1Fkg8iAONcdExt/view?usp=drive_link


**Install Node.js (if not already installed):**  
Download and install from:
```bash
https://nodejs.org/en/download
```



**Install FastAPI**

```bash
pip install "fastapi[standard]"
```

**Navigate into `frontend/src`:**

```bash
cd frontend/src
```

**To install dependencies:**

```bash
npm install
```

**To run frontend:**

```bash
npm run dev
```

**To run backend:**

```bash
python main.py
```


### For Operation

**Controls:**

Click on a piece to select it.
The board will display the possible moves that piece can make.
Click a target position to move the piece.
NOTE: The selected piece must belong to the current player in order to move.

Click on 'New Game' button to end the current game and start a new one.
This works whether the current game has ended or not.


**Gameplay (differences from baseline chess):**

The game does not implement check or checkmate mechanics.
Instead, the King can be attacked directly, and has lives.
The King begins the game with three lives, and loses one every time he is attacked.
When a piece attacks the King, the King remains in its position and the attacking piece returns to its original position.
When a King loses all of its lives, it is captured and its player loses the game.

Advanced moves such as 'castling' and 'en passant' are not allowed in this game.
When a Pawn reaches the opponent's back rank, its player does not select which piece it becomes.
Instead, the Pawn transforms randomly into another piece, in the same way as when it acquires a powerup.
See the Powerup Effects section below for more information on Pawn transformations.

Throughout the game, powerup tokens appear randomly on empty spaces on the board.
Powerups can be obtained by moving onto a space that contains a powerup token, or by capturing a piece with an active powerup.
Powerups are either used on acquisition or on the next move of that piece.
There is only one type of powerup and its effect depends on the type of piece that acquires it.

**Powerup Effects:**

King:
On acquisition of a powerup, the King gains another life, up to a maximum of four.

Queen:
On her next move, the Queen can 'phase' through other pieces.
She can move through any and all other pieces, both friend and foe, along her normal movement paths.
She can attack any enemy piece along those paths, but cannot land on any friendly piece.

Rook:
On its next move, if it captures an enemy piece, the Rook will also capture additional pieces.
It will capture all pieces, both friend and foe, in the immediately adjacent squares in both the horizontal and vertical directions.

Bishop:
On his next move, if the Bishop attacks an enemy piece, instead of capturing the piece the Bishop will 'convert' it.
The attacked piece will change colors and now belong to the attacking player.
The attacked piece will remain in its position, and the attacking Bishop will return to its original position.

Knight:
On his next move, the Knight has additional possible moves along his standard L-shape.
Specifically, the Knight can move one or two spaces in either the horizontal or vertical directions, in addition to his normal movement.

Pawn:
On acquisition of a powerup, the Pawn permanently transforms into another piece.
The Pawn will become either a Knight, a Bishop, a Rook, or a Queen.
The Pawn will not remain a Pawn, and it will not become a King.
