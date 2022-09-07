"""
    Author: Jeff Alkire
    Date:   Sept 7, 2022

    This is the 3rd project form chapter 2 of the text
    Python for First Programs 2nd edition by Kenneth A. Lambert.

    It was assigned in College of the Desert CIS-087 (Python)
"""
PRICE_OLD = 2
PRICE_NEW = 3

old_rentals = int(  input( "  # of $" + str(PRICE_OLD)
                           + ".00 (old) rentals? ")
                 )
new_rentals = int(  input( "  # of $" + str(PRICE_NEW)
                           + ".00 (new) rentals? ")
                 )

total_cost = (PRICE_NEW * old_rentals) + (PRICE_OLD * new_rentals)

print( "Total: $" + str(total_cost) + ".00" )
