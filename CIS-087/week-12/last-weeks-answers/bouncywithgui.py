"""
File: bouncywithgui.py
Project 8.2

Determines the distance traveled by a bouncing ball.

Inputs: Initial height, bounciness index, and number of bounces
"""

from breezypythongui import EasyFrame

def computeDistance(height, index, bounces):
    """Computes the total distance traveled by the ball,
    given an initial height, bounciness index, and
    number of bounces."""
    total = 0
    for x in range(bounces):
        total += height
        height *= index
        total += height
    return total

class BouncyGUI(EasyFrame):

    def __init__(self):
        """Set up the window and widgets."""
        EasyFrame.__init__(self,  title = "Bouncy")
        self.addLabel(text = "Initial height", row = 0, column = 0)
        self.heightField = self.addFloatField(value = 0.0, row = 0, column = 1)
        self.addLabel(text = "Bounciness index", row = 1, column = 0)
        self.indexField = self.addFloatField(value = 0.0, row = 1, column = 1)
        self.addLabel(text = "Number of bounces", row = 2, column = 0)
        self.bouncesField = self.addIntegerField(value = 0, row = 2, column = 1)
        self.addButton(text = "Compute", row = 3, column = 1,
                       columnspan = 2, command = self.computeDistance)
        self.addLabel(text = "Total distance", row = 4, column = 0)
        self.distanceField = self.addFloatField(value = 0.0, row = 4, column = 1)

    def computeDistance(self):
        """Event handler for the Compute button."""
        height = self.heightField.getNumber()
        index = self.indexField.getNumber()
        bounces = self.bouncesField.getNumber()
        distance = computeDistance(height, index, bounces)
        self.distanceField.setNumber(distance)

def main():
    """Instantiate and pop up the window."""
    BouncyGUI().mainloop()

if __name__ == "__main__":
    main()

