console.log(degree15[-1]["exp_cheby"])

document.getElementById('fileInput').addEventListener('change', function(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const content = e.target.result;
        console.log(content)
        console.log(parseCSV(content));
    };
    reader.readAsText(file);
  }
});

function parseCSV(csvData) {
// Split CSV data into rows
const rows = csvData.split('\r\n');
// Get column headers
const headers = rows[0].split(',');
// Initialize an object to hold the parsed data
const parsedData = {};
// Iterate through each row (skipping the header)

for (let i = 1; i < rows.length; i++) {
const values = rows[i].split(',');
// Create an object for each row and push it to the parsedData array
let dataObj = {};

// Map the other values to their corresponding function names
for (let j = 1; j < values.length; j++) {
const headers = ["Degree","exp_taylor","exp_cheby","sin_taylor","sin_cheby","cos_taylor","cos_cheby","tan_taylor","tan_cheby","asin_taylor","asin_cheby","acos_taylor","acos_cheby","atan_taylor","atan_cheby","csc_taylor","csc_cheby","sec_taylor","sec_cheby","cot_taylor","cot_cheby","acsc_taylor","acsc_cheby","asec_taylor","asec_cheby","acot_taylor","acot_cheby"];

dataObj[headers[j]] = parseFloat(values[j]); // Add the value to the object
}
// Push the object for this row to the parsedData array
parsedData[parseFloat(values[0])] = dataObj;
}
return parsedData;
}
