# Taylor-Cheby

*Function approximation with polynomials.*

Project code used for 2025 Massachusetts Science and Engineering Fair project **Analysing the Local Approximation of Trigonometric Functions Using Taylor and Chebyshev Polynomials**.

## Abstract

***Trigonometric functions** are very useful for modeling natural processes, like the swinging of a pendulum, planetary motion, and soundwaves; however, they are not nearly as easy to work with algebraically as polynomial functions. There are many ways of approximating functions, but the two most versatile are the **Taylor** and **Chebyshev polynomials**. The goal of this study is to determine which method of approximation best emulates the original trigonometric function over the range [-1, 1]. This was determined through calculating several metrics of **error** as well as qualitative observations of the data. Python was used to generate the approximations, and they were logged into a spreadsheet. Then, JavaScript was used to calculate error and create visualizations so further observations could be made. The results reveal that in general, the error between the Chebyshev approximation and original function was lower than the error for the Taylor approximation. Therefore, over the interval examined, the Chebyshev polynomial is more effective at approximating trigonometric functions.*

**Keywords:** trigonometric functions, Taylor polynomials, Chebyshev polynomials, error


## Project

Included in this repository are
- Python code used to gather the data concering the approximations
- CSV files containing the raw data itself, as well as several files giving summaries and concise ways to view the data
- A web app used to visualize the data through charts

## API Reference

Several open-source APIs made this project possible.

The **Google Sheets API** was used to plug data generated with Python into a Google Sheet to be exported as a CSV file. Possible without the API, but makes it easier to collect data, process it, then analyze it.

**d3.js** and **HTML Canvas** were used to visualize the data after it had been collected.
 
## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

