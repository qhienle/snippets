// Function to draw a square on the canvas
function drawSquare(x, y, size) {
  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");

  ctx.beginPath();
  ctx.rect(x, y, size, size);
  ctx.fillStyle = "red";
  ctx.strokeStyle = "blue";
  ctx.fill();
  ctx.stroke();
}

// Function to draw a circle on the canvas
function drawCircle(x, y, size) {
  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");

  ctx.beginPath();
  ctx.arc(x, y, size, 0, 2 * Math.PI);
  ctx.fillStyle = "green";
  ctx.strokeStyle = "purple";
  ctx.fill();
  ctx.stroke();
}

// Event listener for clicks on the canvas
const canvas = document.getElementById("canvas");
canvas.addEventListener("click", function(event) {
  // Get click coordinates
  const x = event.clientX;
  const y = event.clientY;
  
  // Randomly choose between square and circle
  if (Math.random() > 0.5) {
    drawSquare(x, y, 50);
  } else {
    drawCircle(x, y, 50);
  }
});
