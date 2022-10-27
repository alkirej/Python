"""
Program: newton.py
Author: Ken

Compute the square root of a number.

1. The input is a number.

2. The outputs are the program's estimate of the square root
   using Newton's method of successive approximations, and
   Python's own estimate using math.sqrt.

Modified: 10-25-22
By:       Jeff Alkire

Complete Project #3 from text chapter 6 page 203.
This requires modifying the recursive function to take a default
value for the original estimate.
"""

import math

# Initialize the tolerance and estimate
TOLERANCE = 0.0000000001

def newton(n: float, est: float = 1.0) -> float:
    next_est = (est + n/est) / 2
    diff = abs(n - next_est**2)

    if diff <= TOLERANCE:
        return next_est
    else:
        return newton(n,next_est)

def main():
    while True:
        # Receive the input number from the user
        ans = input("Enter a positive number: ")
        if 0 == len(ans):
            break
        x = float(ans)

        # Output the result
        print("The program's estimate is", newton(x))
        print("Python's estimate is     ", math.sqrt(x))
        print()

if __name__ == "__main__":
    main()