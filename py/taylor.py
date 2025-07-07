import numpy as np
import matplotlib.pyplot as plt
from sympy import *
import pygsheets
import mpmath as mp
import pandas
from alive_progress import alive_bar

def taylor_approximation(f, a, N, x_symbol):
    """
    Computes the nth-degree Taylor series approximation of `f` at `x = a`.
    \n`T_n(x) = f(a) + f'(a)(x-a) + (f''(a)) / 2! (x-a)^2 + ... + (f^(n)(a)) / n! (x-a)^n`
    
    \n`f` The function being approximated.
    \n`a` The point of approximation.
    \n`N` The degree of the approximation.
    \n`x` SymPy variable.
    """
    approximation = 0
    
    for n in range(N+1):
        # calculate the nth derivative of f at a
        derivative_at_a = diff(f, x_symbol, n).subs(x_symbol, a)
        # calculate nth term of Taylor series
        approximation += derivative_at_a / factorial(n) * (x_symbol - a)**n
    
    return approximation

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
            
            center = 0 # center of Taylor approximation
            
            # Define the range for plotting
            x_values = np.linspace(center - 1, center + 1, 1001) # 1001 evenly spaced values between 0 and 1
            y_values_f = np.array([float(N(f(x))) for x in x_values]) # original function values
            
            # Calculate the Taylor approximation for each x-value
            taylor_poly = taylor_approximation(f(x_symbol), center, degree, x_symbol)
            y_values_taylor = np.array([float(taylor_poly.subs(x_symbol, x).evalf()) for x in x_values])

            # fill Taylor series raw data
            taylor_col = cols[function][0]
            fill_data(sheet, taylor_col+"3:"+taylor_col+"1003", [[y] for y in y_values_f])
            fill_data(sheet, taylor_col+"3:"+taylor_col+"1003", [[y] for y in y_values_taylor])

            bar() # move progress bar to next tick
    
    # Plot the original function and Taylor approximation
    """
    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values_f, label='Original Function', color='blue')
    plt.plot(x_values, y_values_taylor, label=f'Taylor Approximation (degree {degree})', color='red', linestyle='--')
    plt.legend()
    plt.title(f'Taylor Series Approximation of f(x) at x = {center}')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)
    plt.show()"""

if __name__ == '__main__':
    main()
