/* ***************************************** */
/*    If it's used everywhere, it's here.    */
/* ***************************************** */

var canvas = document.getElementById("oth");
var ctx = canvas.getContext("2d");

ctx.mozImageSmoothingEnabled = false;
ctx.imageSmoothingEnabled = false;

// Select the piece counter elements
var numWhiteElement = document.getElementById("numWhite");
var numBlackElement = document.getElementById("numBlack");

var mobile = false;

var cw = canvas.width;
var ch = canvas.height;
var b = 2; // Padding between cells
var gridsize = 75;
var fps = 50;

var board = [];
var color;
var turn = false;
var whiteCount = 0;
var blackCount = 0;
var paused = 0; // 1: paused; 0: not paused
var connected = 0; // 1: connected; 0: not connected
var waiting = 0; // 1: waiting; 0: not waiting
var started = 0; // 1: started; 0: not started

var ws;
var guestId = localStorage.getItem("guestid");
var userId = localStorage.getItem("userid");
var sendBoard = false;

/* ***************************************** */
/*    This is where we'll write basic code   */
/* ***************************************** */

// Updates global variables that track canvas dimensions & mobile device (portrait mode) detection
function obtainScreenInformation() {
	mobile = canvas.height > canvas.width;
	ch = canvas.height;
	cw = canvas.width;
}

// We need to update our globals to reflect our current operating environment.
obtainScreenInformation();
// In case the user is on a mobile device, or is just being odd, let's help them by deteccting resizes:
window.addEventListener("orientationchange", obtainScreenInformation, false);

// Prepare the gameboard and start drawing!
setInterval(draw, 1000 / fps);

/* **************** */
/*      DRAW        */
/* **************** */

// This runs every frame and handles all rendering drawing operations.
function draw() {
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

	// Draw the pieces
	if (board.length == 8 && board[0].length == 8) {
		for (let x = 0; x < 8; x++) {
			for (let y = 0; y < 8; y++) {
				if (board[x][y] == "W") {
					ctx.beginPath();
					ctx.arc(
						x * gridsize + gridsize / 2,
						y * gridsize + gridsize / 2,
						gridsize / 2 - 4 * b,
						0,
						2 * Math.PI
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
	}

	// Start menu code (likely to change over time!)
	if (started == 0) {
		ctx.fillStyle = "#fffa";
		ctx.fillRect(0, 0, cw, ch);

		ctx.font = "30px arial";
		ctx.fillStyle = "#000";
		ctx.textAlign = "center";
		ctx.fillText("Click the Connect button to start the game.", cw / 2, 100);
	}
}

canvas.addEventListener("click", function (event) {
	// This code calculates the location of the canvas, because mouse clicks are not automatically relative to the canvas
	var boundingRect = event.target.getBoundingClientRect();
	var elemLeft = boundingRect.left;
	var elemTop = boundingRect.top;
	var x = event.clientX - elemLeft,
		y = event.clientY - elemTop;

	if (started == 0 || !turn) return;

	// Convert the (x, y) coords to a box on the grid
	var targetX = Math.floor(x / gridsize);
	var targetY = Math.floor(y / gridsize);
	console.log(`Targeting ${targetX} ${targetY}`);

	if (board[targetX][targetY] != "") return;

	// Place a piece!
	// TODO: send placement over WS and render the updated board state
	board[targetX][targetY] = color;
	turn = !turn;

	ws.send(JSON.stringify(board));
});

// The way this code is called will probably change,
document.getElementById("connectBtn").addEventListener("click", function () {
	if (connected) return; // do not reconnect!!
	waiting = 1;

	if (!userId) {
		if (!guestId) {
			guestId = crypto.randomUUID();
			localStorage.setItem("guestid", guestId);
		} else {
			gameId = guestId;
		}
		// TODO different payload based on the user status
	} else {
		gameId = userId;
	}

	gameId = prompt("Enter the game ID to join, or use this one to start a new game", gameId);
	console.log(gameId);
	ws = new WebSocket("ws://localhost:8000/othelloml_api/ws/pvp-session/" + gameId);

	// TODO probably should move these callbacks out of here.  Or maybe not, lol
	ws.onmessage = (event) => {
		var msg = JSON.parse(event.data);
		var boardUpdate = false;

		if (msg.message === "Game is starting..." || msg.message === "picking up game from last state...") {
			waiting = 0;
			started = 1;
			board = msg.game_state;
			boardUpdate = true;
		} else if (msg.message.startsWith("you are player")) {
			color = msg.color;
			turn = color === "B";
		} else if (msg.message === "moved") {
			board = msg.game_state;
			boardUpdate = true;
		}

		if (boardUpdate) {
			blackCount = 0;
			whiteCount = 0;
			for (let x = 0; x < 8; x++) {
				for (let y = 0; y < 8; y++) {
					if (board[x][y] === "B") blackCount++;
					if (board[x][y] === "W") whiteCount++;
				}
			}
			// Change the content of the piece-counters
			numWhiteElement.textContent = "white:  " + whiteCount;
			numBlackElement.textContent = "black:  " + blackCount;
		}

		console.log(msg);
	};

	ws.onopen = (event) => {
		connected = 1;
	};

	ws.onclose = (event) => {
		alert("Connection lost! This might be intentional.");
		connected = 0;
	};

	ws.onerror = (event) => {
		alert("!!!!!!!!!!!!!!!");
		connected = 0;
	};
});
