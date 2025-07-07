function graphError(ctx, error, f) {
  if (window.myChart) {
    window.myChart.destroy();
  }

  const labels = Object.keys(error);
  const taylorData = Object.values(error).map(e => e[f + "_taylor"]);
  const chebyData = Object.values(error).map(e => e[f + "_cheby"]);

  window.myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Taylor Approximation',
          data: taylorData,
          borderColor: 'red',
          fill: false
        },
        {
          label: 'Chebyshev Approximation',
          data: chebyData,
          borderColor: 'blue',
          fill: false
        }
      ]
    },
    options: {
      scales: {
        x: {
          title: {
            display: true,
            text: 'Degree of Approximation'
          },
          grid: {
            display: false
          }
        },
        y: {
          title: {
            display: true,
            text: 'Error'
          },
          grid: {
            display: false
          }
        }
      }
    }
  });
}

const Esubmit = document.getElementById("Esubmit");
Esubmit.addEventListener("click", (e) => {
  e.preventDefault();
  updateEGraph();
});

function updateEGraph() {
  const Egraph = document.getElementById("Egraph");
  const Ectx = Egraph.getContext("2d");
  Ectx.clearRect(-graph.width, -graph.height, graph.width * 10, graph.height * 10);
  const f = document.getElementById("Efunction").value;
  const error = document.getElementById("Eerror").value;
  let errorData;
  switch (error) {
    case "rmse":
      errorData = rmse;
      break;
    case "mape":
      errorData = mape;
      break;
    case "r_squared":
      errorData = r_squared;
      break;
  }
  Ectx.clearRect(-graph.width, -graph.height, graph.width * 2, graph.height * 2);
  
  Ectx.setTransform(1, 0, 0, 1, 0, 0);
  Ectx.translate(10, offset.y * 2 - 10);

  graphError(Ectx, errorData, f);
}