"""
File: bouncywithgui.py
Project 8.2
Author: Dylan Williams

Determines the distance total traveled by a bouncing ball.

Input values: Initial height, bounciness index, and number of bounces
"""

from breezypythongui import EasyFrame

def computeDistance(height, index, bounces):
    """Calculates the total distance traveled by the ball, given
    the initial height, bounciness index, and total number of bounces."""
    Total = 0
    for x in range(bounces):
        Total += height
        height *= index
        Total += height
    return Total

class BouncyGUI(EasyFrame):

    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, title = "Bouncy")
        self.addLabel(text = "Initial Height", row = 0, column = 0)
        self.heightField = self.addFloatField(value = 0.0, row = 0, column = 1)
        self.addLabel(text = "Bounciness Index", row = 1, column = 0)
        self.indexField =  self.addFloatField(value = 0.0, row = 1, column = 1)
        self.addLabel(text = "Number of Bounces", row = 2, column = 0)
        self.bouncesField = self.addIntegerField(value = 0, row = 2, column = 1)
        self.addButton(text = "Compute", row = 3, column = 1,
                       columnspan = 2, command = self.computeDistance)
        self.addLabel(text = "Total Distance", row = 4, column = 0)
        self.distanceField = self.addFloatField(value = 0.0, row = 4, column = 1)

    def computeDistance(self):
        """Event handler for the Compute button."""
        height = self.heightField.getNumber()
        index = self.indexField.getNumber()
        bounces = self.bouncesField.getNumber()
        distance = computeDistance(height, index, bounces)
        self.distanceField.setNumber(distance)

def main():
    """Instantiate and bring up the window."""
    BouncyGUI().mainloop()

if __name__ == "__main__":
    main()