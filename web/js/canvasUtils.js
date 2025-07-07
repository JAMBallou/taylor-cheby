function adjustCanvasScale(ctx, f) {
  switch (f) {
    case "exp":
      ctx.translate(0, graph.height / 2);
      drawCoordinateSystem(ctx, offset);
      drawLabels(ctx, f, offset, verticalShift = graph.height / 2);
      break;
    case "acos":
      ctx.translate(0, graph.height / 2);
      drawCoordinateSystem(ctx, offset);
      drawLabels(ctx, f, offset, verticalShift = graph.height / 2);
      break;
    case "sec":
      ctx.translate(0, graph.height / 4);
      drawCoordinateSystem(ctx, offset);
      drawLabels(ctx, f, offset, verticalShift = graph.height / 4);
      break;
    case "csc":
      ctx.translate(0, graph.height / 4);
      drawCoordinateSystem(ctx, offset);
      drawLabels(ctx, f, offset, verticalShift = graph.height / 4);
      break;
    case "cot":
      ctx.translate(0, -graph.height / 4);
      drawCoordinateSystem(ctx, offset);
      drawLabels(ctx, f, offset, verticalShift = graph.height / 4);
      break;
    case "acot":
      ctx.translate(0, graph.height / 4);
      drawCoordinateSystem(ctx, offset);
      drawLabels(ctx, f, offset, verticalShift = graph.height / 4);
      break;  
    default:
      drawCoordinateSystem(ctx, offset);
      drawLabels(ctx, f, offset); 
  }
}

function adjustErrorCanvasScale(ctx, f) {
  switch (f) {
    case "sin":
      return 0;
    case "tan":
      return 0;
    case "asin":
      return 0;
    case "acos":
      return 75;
    case "atan":
      return 0;
    case "cot":
      return -50;
    case "acsc":
      return 25;
    default:
      return 50;
  }
}

function drawLabels(ctx, f, offset, verticalShift = 0, horizontalShift = 0) {
  ctx.font = "12px Arial";
  ctx.fillStyle = "black";
  ctx.textAlign = "center";

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
      ctx.fillText((-i / 250).toFixed(1), -5, i + 3);
    }
  }
  
  // f(x) labels
  ctx.textAlign = "left";
  ctx.font = "bold 15px Helvetica";
  ctx.fillText("f(x) = " + f + "(x)", -graph.width / 2 + 20 - horizontalShift, -graph.height / 2 + 25 - verticalShift);
  ctx.fillStyle = "red";
  ctx.fillText("Taylor Approximation", -graph.width / 2 + 20 - horizontalShift, -graph.height / 2 + 50 - verticalShift);
  ctx.fillStyle = "blue";
  ctx.fillText("Chebyshev Approximation", -graph.width / 2 + 20 - horizontalShift, -graph.height / 2 + 75 - verticalShift);
}

function drawCoordinateSystem(ctx, offset) {
  ctx.fillStyle = "black";
  ctx.font = "12px Arial";
  ctx.beginPath();
  ctx.moveTo(-offset.x - 500, 0);
  ctx.lineTo(ctx.canvas.width - offset.x + 500, 0);
  ctx.moveTo(0, -offset.y - 500);
  ctx.lineTo(0, ctx.canvas.height - offset.y + 500);
  ctx.lineWidth = 1;
  ctx.strokeStyle = "gray";
  ctx.stroke();
  ctx.setLineDash([]);
}