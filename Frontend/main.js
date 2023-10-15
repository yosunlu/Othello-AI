/* ***************************************** */
/*    If it's used everywhere, it's here.    */
/* ***************************************** */

var canvas = document.getElementById("oth");
var ctx = canvas.getContext("2d");

ctx.mozImageSmoothingEnabled = false;
ctx.imageSmoothingEnabled = false;

var mobile = false;
let turn = "w"; // delete when implementing PVP

var elemLeft = canvas.offsetLeft;
var elemTop = canvas.offsetTop;
var cw = canvas.width;
var ch = canvas.height;
var b = 2; // Padding between cells
var gridsize = 75;
var fps = 5; // Frames per second (movement will NOT be smooth)

var board = [];
var pause = 0; // 1: paused; 0: not paused

/* ***************************************** */
/*    This is where we'll write basic code   */
/* ***************************************** */

function obtainScreenInformation() {
	mobile = canvas.height > canvas.width;
	ch = canvas.height;
	cw = canvas.width;
}

function start() {
	pause = 0;
	board = [];

	for (let i = 0; i < 8; i++) {
		board[i] = ["", "", "", "", "", "", "", ""];
	}

	board[3][3] = "w";
	board[4][3] = "b";
	board[4][4] = "w";
	board[3][4] = "b";
}

// We need to update our globals to reflect our current operating environment.
obtainScreenInformation();
// In case the user is on a mobile device, or is just being odd, let's help them by resizing:
window.addEventListener("orientationchange", obtainScreenInformation, false);
start();
setInterval(draw, 1000 / fps);

/* **************** */
/*      DRAW        */
/* **************** */
function draw() {
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

	// Draw the weird little circles
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
	for (let x = 0; x < 8; x++) {
		for (let y = 0; y < 8; y++) {
			if (board[x][y] == "w") {
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
			} else if (board[x][y] == "b") {
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

canvas.addEventListener("click", function (event) {
	var x = event.pageX - elemLeft,
		y = event.pageY - elemTop;

	var targetX = Math.floor(x / gridsize);
	var targetY = Math.floor(y / gridsize);

	if (board[targetX][targetY] != "") return;

	board[targetX][targetY] = turn;
	turn = turn == "w" ? "b" : "w";
});

document.getElementById("newGameBtn").addEventListener("click", function () {
	start();
});
