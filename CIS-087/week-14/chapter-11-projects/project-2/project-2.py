"""
Author: Jeff Alkire
Date:   11-30-2022
Purpose:    Complete project #2 from chapter 11 of the text:
                Write a function to reverse the elements in a list.
"""



def reverse(ls):
    """
    Reverse the contents of a list. Note: no error checking is implemented.
    :param ls: List to reverse
    :return: a copy of the list in reverse order
    """
    return_val = []
    for idx in range(len(ls)-1,0,-1):
        current = ls[idx]
        return_val.append(current)
    return return_val


test_list = ["one","two","three","four","five","six","seven","eight","nine","ten"]
new_list = reverse(test_list)

print("Original List:")
print("==============")
print(test_list)
print()
print("Reversed List:")
print("==============")
print(new_list)