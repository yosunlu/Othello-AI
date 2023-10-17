/* ***************************************** */
/*    If it's used everywhere, it's here.    */
/* ***************************************** */

var canvas = document.getElementById("oth");
var ctx = canvas.getContext("2d");

ctx.mozImageSmoothingEnabled = false;
ctx.imageSmoothingEnabled = false;

var mobile = false;
let turn = "W"; // delete when implementing PVP

var cw = canvas.width;
var ch = canvas.height;
var b = 2; // Padding between cells
var gridsize = 75;
var fps = 50; // Frames per second (movement will NOT be smooth)

var board = [];
var pause = 0; // 1: paused; 0: not paused
var started = 0; // 1: started; 0: not started

var ws;
var gameId = crypto.randomUUID();

/* ***************************************** */
/*    This is where we'll write basic code   */
/* ***************************************** */

function obtainScreenInformation() {
	mobile = canvas.height > canvas.width;
	ch = canvas.height;
	cw = canvas.width;
}

function init() {
	pause = 0;
	board = [];

	for (let i = 0; i < 8; i++) {
		board[i] = ["", "", "", "", "", "", "", ""];
	}

	board[3][3] = "W";
	board[4][3] = "B";
	board[4][4] = "W";
	board[3][4] = "B";
}

// We need to update our globals to reflect our current operating environment.
obtainScreenInformation();
// In case the user is on a mobile device, or is just being odd, let's help them by resizing:
window.addEventListener("orientationchange", obtainScreenInformation, false);

init();
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
	var boundingRect = event.target.getBoundingClientRect();
	var elemLeft = boundingRect.left;
	var elemTop = boundingRect.top;
	var x = event.clientX - elemLeft,
		y = event.clientY - elemTop;

	var targetX = Math.floor(x / gridsize);
	var targetY = Math.floor(y / gridsize);

	if (started == 0) return;
	console.log(`Targeting ${targetX} ${targetY}`);

	if (board[targetX][targetY] != "") return;

	board[targetX][targetY] = turn;
	turn = turn == "W" ? "B" : "W";
});

document.getElementById("connectBtn").addEventListener("click", function () {
	init();

	started = 1;
	ws = new WebSocket("wss://localhost/ws/pvp-session/" + gameId);

	// TODO probably should move these callbacks out of here.  Or maybe not, lol
	ws.onmessage = (event) => {
		var msg = JSON.parse(event.data);

		console.log(msg);
	};

	ws.onopen = (event) => {
		ws.send();
	};

	ws.onclose = (event) => {
		alert("Connection lost! This might be intentional.");
	};

	ws.onerror = (event) => {
		alert("!!!!!!!!!!!!!!!");
	};
});
