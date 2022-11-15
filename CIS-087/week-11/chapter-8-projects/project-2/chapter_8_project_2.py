"""
Author: Jeff Alkire
Date:   Nov 3, 2022

Project 2 from Chapter 8 of the text.  Implement Project 4 from chapter 3
(page 99) using a GUI interface.

Given a height, bounciness percentage of object, and number of bounces,
calculate the distance travelled by the object.
"""

from breezypythongui import EasyFrame

class BouncyFrame(EasyFrame):
    def __init__(self):
        """
        Setup widgets on window
        """
        EasyFrame.__init__(self)
        self.addLabel(text="Initial Height (in Feet):",
                      row=0,
                      column=0,
                      sticky="NW"
                      )
        self.height = self.addFloatField \
            (value=0,
             row = 0,
             column = 1,
             sticky = "NW"
             )

        self.addLabel(text="Bounciness (0-1):",
                      row=2,
                      column=0,
                      sticky="NW"
                      )
        self.bounciness = self.addFloatField \
            (value=0.5,
             row = 2,
             column = 1,
             sticky = "NW"
             )

        self.addLabel(text="Bounces:",
                      row=3,
                      column=0,
                      sticky="NW"
                      )
        self.bounces = self.addIntegerField \
            (value=0,
             row = 3,
             column = 1,
             sticky = "NW"
             )
        self.addLabel(text="Distance Traveled:",
                      row=5,
                      column=0,
                      sticky="NW"
                      )
        self.distance = self.addFloatField \
            (value=0.0,
             row = 5,
             column = 1,
             precision=2,
             state="readonly"
             )

        self.addButton(text = "Calculate Distance Traveled",
                       row = 4, column = 0,
                       columnspan = 2,
                       command = self.compute
                       )

    # Methods to handle user events.
    def compute(self):
        """
        Calculate tax and update tax box on the screen.
        """
        ht  = self.height.getNumber()
        if ht < 0:
            self.height.setNumber(0.0)
        bcs = self.bounces.getNumber()
        if bcs < 0:
            self.bounces.setNumber(0)
        bn  = self.bounciness.getNumber()
        if bn < 0.0:
            self.bounciness.setNumber(0.0)
        elif bn > 1.0:
            self.bounciness.setNumber(1.0)

        tot_dist = 0.0
        for n in range(bcs):
            tot_dist += ht
            ht *= bn
            tot_dist += ht

        self.distance.setNumber(tot_dist)

def main():
    """ Instantiate window and start gui loop. """
    BouncyFrame().mainloop()

if __name__ == "__main__":
    main()