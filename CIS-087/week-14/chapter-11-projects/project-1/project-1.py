"""
Author: Jeff Alkire
Date:   11-30-2022
Purpose:    Complete project #1 from chapter 11 of the text:
                Do a sequential search of a list stopping if
                the item has been passed.
"""


def modified_sequential_search(ls, find_me):
    """
    Search for an item in a list returning its index (or -1 if not found)
    :param ls: the least to search
    :param find_me: the item to search for
    :return: the index of find_me in the list or -1 if not found.
    """
    for idx in range(len(ls)):
        l = ls[idx]
        if find_me <= l:
            if find_me == l:
                return idx
            else:
                return -1
    return -1

test_list = ["one","two","three","four","five","six","seven","eight","nine","ten"]
test_list.sort()

print(test_list)
print()
six = modified_sequential_search(test_list,"six")
print( "index of six: %d" % six)
twelve = modified_sequential_search(test_list,"twelve")
print( "index of twelve: %d" % twelve)
