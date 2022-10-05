"""
    Program:  Chapter 5 Project 1
    Author:   Jeff Alkire
    Date:     October 3, 2021
"""

def mode( num_list: [int] ) -> int:
    occurs = {}
    for n in num_list:
        cnt = occurs.get( n, 0)
        occurs[n] = cnt + 1

    max_so_far  = occurs[ num_list[0] ]
    mode_so_far = num_list[0]
    for k in occurs:
        cnt = occurs[k]
        if cnt > max_so_far:
            max_so_far = cnt
            mode_so_far = k

    return mode_so_far

def median( num_list: [int] ) -> float:
    num_list.sort()
    if len(num_list) % 2 == 1:
        midpt = len(num_list) // 2
        return num_list[midpt]
    else:
        midpt = len(num_list) // 2
        return (num_list[midpt] + num_list[midpt-1]) / 2

def mean( num_list: [int] ) -> float:
    total = 0
    for n in num_list:
        total += n
    return total / len(num_list)

def main():
    test_list = [ 94,  5,  20, -14,  94,
                  34, 37,  46,  35, 100,
                 -88, 33,  88,  36,  20,
                  33,  5, -14, 200,  94
                ]

    print( "Mode:   %5d" % mode(test_list) )
    print( "Median: %7.1f" % median(test_list) )
    print( "Mean:   %7.1f" % mean(test_list) )

if __name__ == "__main__":
    main()