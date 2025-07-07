import numpy as np
import mpmath as mp
import pandas
import pygsheets
from alive_progress import alive_bar

def rmse(y_pred, y_true):
    # calculate Root Mean Squared Error
    # RMSE = sqrt(1/N sum((Y_n - Y^_n)^2))
    return np.sqrt(np.mean((y_pred - y_true) ** 2))

def mape(y_pred, y_true):
    # calculate Mean Absolute Percentage Error
    # MAPE = 100/N sum(|(Y_n - Y^_n) / Y_n|)
    # mask for non-zero y_true values
    mask = y_true != 0
    y_true_nonzero = y_true[mask]
    y_pred_nonzero = y_pred[mask]
    
    # Calculate MAPE
    return np.mean(np.abs((y_pred_nonzero - y_true_nonzero) / y_true_nonzero)) * 100

def r_squared(y_pred, y_true):
    # calculate R-Squared
    # R^2 = 1 - (sum((Y_n - Y^_n)^2)) / (sum((Y_n - Y-)^2))
    # calculate the residual sum of squares (RSS) and total sum of squares (TSS)
    ss_residual = np.sum((y_true - y_pred) ** 2)
    ss_total = np.sum((y_true - np.mean(y_true)) ** 2)

    return 1 - (ss_residual / ss_total)

def error(y_pred, y_true):
    """
    Calculate error in three ways: RMSE, MAPE, and R^2.
    \n`y_pred` The predicted data value (the approximation).
    \n`y_true` The original, actual data value.
    """

    # calculates formatted error to 4 decimal places (rounded)
    errors = [f"{rmse(y_pred, y_true):.4f}", f"{mape(y_pred, y_true):.4f}", f"{r_squared(y_pred, y_true):.4f}"]
    return errors

def fetch_data(active_sheet, col):
    """
    Function to fetch data from the data spreadsheet and calculate the error.
    \n`active_sheet` The sheet from which data is received.
    \n`col` Group from which the data is received: exp(x) - 0, sin(x) - 1, etc.
    """
    # possible columns to retrieve data from
    cols = [["B", "C", "D"], ["E", "F", "G"], ["H", "I", "J"], ["K", "L", "M"], ["N", "O", "P"], ["Q", "R", "S"], ["T", "U", "V"], ["W", "X", "Y"], ["Z", "AA", "AB"], ["AC", "AD", "AE"], ["AF", "AG", "AH"], ["AI", "AJ", "AK"], ["AL", "AM", "AN"]]
    wks = sh[active_sheet]
    true_col = cols[col][0]
    taylor_col = cols[col][1]
    cheby_col = cols[col][2]
    # find the true and predicted datasets
    y_true_taylor = np.array([float(*x) for x in wks.get_values(true_col+"3", true_col+"1003", returnas="matrix")])
    y_pred_taylor = np.array([float(*x) for x in wks.get_values(taylor_col+"3", taylor_col+"1003", returnas="matrix")])
    y_true_cheby = np.array([float(*x) for x in wks.get_values(true_col+"3", true_col+"1003", returnas="matrix")])
    y_pred_cheby = np.array([float(*x) for x in wks.get_values(cheby_col+"3", cheby_col+"1003", returnas="matrix")])

    e_taylor = error(y_pred_taylor, y_true_taylor)
    e_cheby = error(y_pred_cheby, y_true_cheby)
    return [e_taylor, e_cheby]

def fill_error(e, col):
    """
    Function that uses the calculated error and inputs it into the correct spreadsheet.
    \n`e` The error data: `[rmse, mape, r_squared]`.
    \n`col` The column in which the error data is entered: exp(x) - 0, sin(x) - 1, etc.
    """
    cols = [["C", "D"], ["E", "F"], ["G", "H"], ["I", "J"], ["K", "L"], ["M", "N"], ["O", "P"], ["Q", "R"], ["S", "T"], ["U", "V"], ["W", "X"], ["Y", "Z"], ["AA", "AB"]]
    row = 1 + 3 * active_sheet
    taylor_error_col = cols[col][0]
    cheby_error_col = cols[col][1]
    wks = sh[0]
    # fill in data based on params
    wks.update_value(taylor_error_col+str(row), e[0][0])
    wks.update_value(taylor_error_col+str(row+1), e[0][1])
    wks.update_value(taylor_error_col+str(row+2), e[0][2])
    wks.update_value(cheby_error_col+str(row), e[1][0])
    wks.update_value(cheby_error_col+str(row+1), e[1][1])
    wks.update_value(cheby_error_col+str(row+2), e[1][2])

gc = pygsheets.authorize(service_file="keys/client_secret.json") # set API key
sh = gc.open_by_key("1ZchKElVGKmHQvF8TuLNKTlRGkoQ5z-ek1-9kWh9THIA") # URL

# ensure chosen sheet is within bounds
active_sheet = int(input("Pick data spreadsheet/degree: "))
if active_sheet < 0 or active_sheet > 14: 
    active_sheet = 1
    print("Input too large/small. Changed to 1.")
wks = sh[active_sheet] # input sheet number here (first is 0)

with alive_bar(13) as bar: # setup progress bar
    # execute error calculations and fill data for all functions
    for i in range(0, 13):
        
        e = fetch_data(active_sheet, i)
        fill_error(e, i)

        bar()