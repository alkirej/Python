"""
Author: Jeff Alkire
Date:   11-30-2022
Purpose:    Complete project #3 from chapter 11 of the text:
                Implement an exponent function.
"""

def expo( base, exponent ):
    result = 1
    for n in range(exponent):
        result *= base

    return result

print(" 6 ^  6 = %d" % expo(6,6))
print(" 2 ^ 10 = %d" % expo(2,10))
print(" 8 ^  3 = %d" % expo(8,3))