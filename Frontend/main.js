/* ***************************************** */
/*    If it's used everywhere, it's here.    */
/* ***************************************** */

var canvas = document.getElementById("oth");
var ctx = canvas.getContext("2d");

var cw = canvas.width;
var ch = canvas.height;
var b = 2; // Padding between cells
var fps = 5; // Frames per second (movement will NOT be smooth)
var pause = 0; // 1: paused; 0: not paused

var gridsize = 75;

/* ***************************************** */
/*    This is where we'll write basic code   */
/* ***************************************** */

function start() {
	pause = 0;
}

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
}
