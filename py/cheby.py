import numpy as np
import matplotlib.pyplot as plt
from sympy import *
import pygsheets
import mpmath as mp
import pandas
from alive_progress import alive_bar
from numpy.polynomial.chebyshev import Chebyshev

def chebyshev_approximation(f, a, b, N, x_symbol):
    """
    Computes the nth-degree Chebyshev series approximation of `f` on the interval [a, b].
    
    \n`f` The function being approximated.
    \n`a` The start of the interval.
    \n`b` The end of the interval.
    \n`N` The degree of the approximation.
    \n`x` SymPy variable.
    """
    # Create a lambda function for numerical evaluation
    f_lambda = lambdify(x_symbol, f, 'numpy')
    
    # Generate Chebyshev nodes
    x = np.linspace(a, b, 100)
    y = f_lambda(x)
    
    # Fit Chebyshev polynomial
    cheby_poly = Chebyshev.fit(x, y, N)
    cheby_expr = Chebyshev(cheby_poly.coef)
    
    # Convert Chebyshev polynomial to SymPy expression
    #cheby_expr = sum(c * (x_symbol**i) for i, c in enumerate(cheby_poly.coef))
    
    return cheby_expr

# shift trig functions undefined at 0
def shifted_csc(x): return csc(x + 2)
def shifted_cot(x): return cot(x + 2)
def shifted_acsc(x): return acsc(x + 2)
def shifted_asec(x): return asec(x + 2)
def shifted_acot(x): return acot(x + 1)

def fill_data(sheet, range, data):
    """
    Fills data into a google sheet.
    \n`sheet` The sheet number:
    \n\t0 - Error
    \n\t1-10, 15, 20, 25 - Degree approximation no.
    \n`range` Data range to fill with values; format `A5:A10`.
    \n`data` Dataset to fill into cells (matrix) - shape of `data` must match `range`.
    """

    gc = pygsheets.authorize(service_file="keys/client_secret.json") # set API key
    sh = gc.open_by_key("1ZchKElVGKmHQvF8TuLNKTlRGkoQ5z-ek1-9kWh9THIA") # URL

    wks = sh[sheet] # input sheet number here (first is 0)

    wks.update_values(range, data)

def main():
    # define sympy variable
    x_symbol = symbols('x')
    # choose sheet where data will be entered
    sheet = int(input("Enter desired sheet / degree of approximation: "))
    # logic for incorrect and large values entered
    if sheet < 0 or sheet > 13: 
        sheet = 1
        print("Input too large/small. Changed to 1.")
    degree = sheet
    if degree == 11: 
        degree = 15
        print("Degree changed to 15")
    if degree == 12: 
        degree = 20
        print("Degree changed to 20")
    if degree == 13: 
        degree = 25
        print("Degree changed to 25")
    # ordered list of possible functions to approximate
    target_functions = [exp, sin, cos, tan, asin, acos, atan, shifted_csc, sec, shifted_cot, shifted_acsc, shifted_asec, shifted_acot]
    # column labels of data columns
    cols = [["C", "D"], ["F", "G"], ["I", "J"], ["L", "M"],["O", "P"], ["R", "S"],["U", "V"], ["X", "Y"],["AA", "AB"], ["AD", "AE"],["AG", "AH"], ["AJ", "AK"], ["AM", "AN"]]

    with alive_bar(len(target_functions)) as bar: # setup progress bar
        for function in range(0, len(target_functions)):
            # main loop to approximate all functions in given sheet
            f = target_functions[function] # accesses function list and picks one based on input
            
            center = 0 # center of Chebyshev approximation
            
            # Define the range for plotting
            x_values = np.linspace(center - 1, center + 1, 1001) # 1001 evenly spaced values between 0 and 1
            y_values_f = np.array([float(N(f(x))) for x in x_values]) # original function values
            
            # Calculate the Taylor approximation for each x-value
            cheby_poly = chebyshev_approximation(f(x_symbol), -1, 1, degree, x_symbol)
            y_values_cheby = cheby_poly(x_values)

            # fill Taylor series raw data
            cheby_col = cols[function][1]
            fill_data(sheet, cheby_col+"3:"+cheby_col+"1003", [[y] for y in y_values_f])
            fill_data(sheet, cheby_col+"3:"+cheby_col+"1003", [[y] for y in y_values_cheby])

            bar() # move progress bar to next tick
    
            # Plot the original function and Taylor approximation
            """plt.figure(figsize=(8, 6))
            plt.plot(x_values, y_values_f, label='Original Function', color='blue')
            plt.plot(x_values, y_values_cheby, label=f'Chebyshev Approximation (degree {degree})', color='red', linestyle='--')
            plt.legend()
            plt.title(f'Chebyshev Series Approximation of f(x) at x = {center}')
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.grid(True)
            plt.show()"""

if __name__ == '__main__':
    main()
