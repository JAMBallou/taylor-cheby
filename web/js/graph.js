const graph = document.getElementById("graph");
const ctx = graph.getContext("2d");

const errorGraph = document.getElementById("absoluteError");
const errorCtx = errorGraph.getContext("2d");

const offset = {
  x: graph.width / 2,
  y: graph.height / 2
}; 

ctx.translate(offset.x, offset.y);
errorCtx.translate(offset.x, offset.y);

const submit = document.getElementById("submit");
submit.addEventListener("click", (e) => {
  e.preventDefault();
  const f = document.getElementById("function").value;
  const degree = degrees[Number(document.getElementById("degree").value) - 1];
  ctx.clearRect(-graph.width, -graph.height, graph.width * 2, graph.height * 2);
  errorCtx.clearRect(-graph.width, -graph.height, graph.width * 2, graph.height * 2);
  
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  errorCtx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.translate(offset.x, offset.y);
  errorCtx.translate(offset.x, offset.y);

  adjustCanvasScale(ctx, f);
  graphSystem(ctx, degree, f);
  graphAbsoluteError(errorCtx, degree, f);
});

const f = "exp";
const degrees = [degree1, degree2, degree3, degree4, degree5, degree6, degree7, degree8, degree9, degree10, degree15, degree20, degree25];
adjustCanvasScale(ctx, f);
graphSystem(ctx, degree1, f);
graphAbsoluteError(errorCtx, degree1, f);

function graphSystem(ctx, degree, f) {
  graphFunction(ctx, degree, f + "_true", "black");
  graphFunction(ctx, degree, f + "_taylor", "red");
  graphFunction(ctx, degree, f + "_cheby", "blue");
}

function graphFunction(ctx, degree, f, color = "black") {
  for (let i in degree) {
    const x = i * 250;
    const y = -degree[i][f] * 250;
    ctx.beginPath();
    ctx.arc(x, y, 1, 0, 2 * Math.PI);
    ctx.fillStyle = color;
    ctx.fill();
  }
}

function graphAbsoluteError(ctx, degree, f) {
  const errorOffset = adjustErrorCanvasScale(ctx, f);
  drawCoordinateSystem(ctx, offset);

  // X-axis labels
  for (let i = -offset.x; i <= ctx.canvas.width - offset.x; i += 50) {
    if (i !== 0) {
      ctx.fillText((i / 250).toFixed(1), i, 15);
    }
  }

  // Y-axis labels
  ctx.textAlign = "right";
  for (let i = -offset.y - 500; i <= ctx.canvas.height - offset.y + 500; i += 50) {
    if (i !== 0) {
      ctx.fillText((-i / 1000).toFixed(3), -5, i + 3);
    }
  }
  
  // f(x) labels
  ctx.textAlign = "left";
  ctx.font = "bold 15px Helvetica";
  ctx.fillStyle = "red";
  ctx.fillText("f(x) - Taylor Approximation(x)", -graph.width / 2 + 20, -graph.height / 2 + 25);
  ctx.fillStyle = "blue";
  ctx.fillText("f(x) - Chebyshev Approximation(x)", -graph.width / 2 + 20, -graph.height / 2 + 50);

  for (let i in degree) {
    const x = i * 250;
    const y_true = -degree[i][f + "_true"] * 1000;
    const y_taylor = -degree[i][f + "_taylor"] * 1000;
    const y_cheby = -degree[i][f + "_cheby"] * 1000;
    
    ctx.beginPath();
    ctx.fillStyle = "red";
    ctx.arc(x, y_true - y_taylor, 1, 0, 2 * Math.PI);
    ctx.fill();
    ctx.beginPath();
    ctx.fillStyle = "blue";
    ctx.arc(x, y_true - y_cheby, 1, 0, 2 * Math.PI);
    ctx.fill();
  }
}