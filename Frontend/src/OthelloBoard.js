import React, { useEffect, useRef, useState } from "react";

const OthelloBoard = (props) => {
  const { started, onDataChange, whiteCount, blackCount } = props;
  const canvasRef = useRef(null);
  const [board, setBoard] = useState([]);
  const [turn, setTurn] = useState("W");
  // b and grid size initialized as global var becaues both useEffect and drawPieces use it
  const [b, setB] = useState(2);
  const gridsize = 75;
  var white = whiteCount;
  var black = blackCount;

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    var cw = canvas.width;
    var ch = canvas.height;
    var fps = 10;

    var paused = 0; // 1: paused; 0: not paused

    function init() {
      paused = 0;

      for (let i = 0; i < 8; i++) {
        board[i] = ["", "", "", "", "", "", "", ""];
      }

      if (started) {
        board[3][3] = "W";
        board[4][3] = "B";
        board[4][4] = "W";
        board[3][4] = "B";
      }

      // Without this, previous frames remain on the screen
      ctx.clearRect(0, 0, cw, ch);

      // Background
      ctx.fillStyle = "green";
      ctx.fillRect(0, 0, cw, ch);

      ctx.fillStyle = "black";

      // Draw the lines
      for (var d1 = 0; d1 < 602; d1 += gridsize) {
        ctx.fillRect(d1, 0, b, ch);
        ctx.fillRect(0, d1, cw, b);
      }

      // Draw the 4 weird little circles around the middle 4 squares:
      ctx.beginPath();
      ctx.arc(150 + b / 2, 150 + b / 2, 3 * b, 0, 3 * Math.PI);
      ctx.fill();
      ctx.closePath();

      ctx.beginPath();
      ctx.arc(150 + b / 2, 452 - b / 2, 3 * b, 0, 3 * Math.PI);
      ctx.fill();
      ctx.closePath();
      ctx.beginPath();

      ctx.arc(452 - b / 2, 150 + b / 2, 3 * b, 0, 3 * Math.PI);
      ctx.fill();
      ctx.closePath();

      ctx.beginPath();
      ctx.arc(452 - b / 2, 452 - b / 2, 3 * b, 0, 3 * Math.PI);
      ctx.fill();
      ctx.closePath();

      // Start menu code (likely to change over time!)
      if (started == 0) {
        ctx.fillStyle = "#fffa";
        ctx.fillRect(0, 0, cw, ch);

        ctx.font = "30px arial";
        ctx.fillStyle = "#000";
        ctx.textAlign = "center";
        ctx.fillText(
          "Click the Connect button to start the game.",
          cw / 2,
          100
        );
      }
    }

    init();
    setInterval(draw, 1000 / fps);

    /* **************** */
    /*      DRAW        */
    /* **************** */

    // This runs every frame and handles all rendering drawing operations.
    function draw() {
      // Draw the pieces
      drawPieces(ctx);
    }
  }, [started]);

  const drawPieces = (ctx) => {
    for (let x = 0; x < 8; x++) {
      for (let y = 0; y < 8; y++) {
        if (board[x][y] == "W") {
          ctx.beginPath();
          ctx.arc(
            // define the circle
            x * gridsize + gridsize / 2,
            y * gridsize + gridsize / 2,
            gridsize / 2 - 4 * b, // radius
            0, // startAngle
            2 * Math.PI // endAngle
          );
          ctx.fillStyle = "white";
          ctx.fill();
          ctx.closePath();
        } else if (board[x][y] == "B") {
          ctx.beginPath();
          ctx.arc(
            x * gridsize + gridsize / 2,
            y * gridsize + gridsize / 2,
            gridsize / 2 - 4 * b,
            0,
            2 * Math.PI
          );
          ctx.fillStyle = "black";
          ctx.fill();
          ctx.closePath();
        }
      }
    }
  };

  const handleCanvasClick = (event) => {
    const canvas = canvasRef.current;
    const boundingRect = canvas.getBoundingClientRect();
    const x = event.clientX - boundingRect.left;
    const y = event.clientY - boundingRect.top;

    if (started === 0) return;

    const targetX = Math.floor(x / gridsize);
    const targetY = Math.floor(y / gridsize);

    if (board[targetX][targetY] !== "") return;

    const newBoard = [...board]; // newBoard will be a new array containing all the elements of the board array
    newBoard[targetX][targetY] = turn;
    setBoard(newBoard);

    const newTurn = turn === "W" ? "B" : "W";
    setTurn(newTurn);

    if (turn === "W") {
      white++;
    } else {
      black++;
    }

    onDataChange(white, black);
  };

  return (
    <canvas
      ref={canvasRef}
      width={602}
      height={602}
      onClick={handleCanvasClick}
    />
  );
};

export default OthelloBoard;
