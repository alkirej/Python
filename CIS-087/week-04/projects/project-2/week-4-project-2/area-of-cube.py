"""
    Author: Jeff Alkire
    Date:   Sept 7, 2022

    This is the 2nd project form chapter 2 of the text
    Python for First Programs 2nd edition by Kenneth A. Lambert.

    It was assigned in College of the Desert CIS-087 (Python)
"""

edge_len = int( input( "How long is each edge of this cube? ") )

# formula for surface area of a cube = 6 times the square of length of an edge.
surface_area_of_cube = 6 * (edge_len ** 2)
print ( "The surface area of our cube is: ", end="")
print ( surface_area_of_cube, end="" )
print ( " units squared." )