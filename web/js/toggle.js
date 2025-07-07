const toggle = document.querySelector("#toggle input");
toggle.addEventListener("change", (e) => {
  const functionGraphContainer = document.getElementById("functionGraphContainer");
  const errorGraphContainer = document.getElementById("errorGraphContainer");
  functionGraphContainer.style.display = e.target.checked ? "block" : "none";
  errorGraphContainer.style.display = e.target.checked ? "none" : "block";
  updateEGraph();
});