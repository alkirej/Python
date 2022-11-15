"""
Author: Jeff Alkire
Date:   Nov 2, 2022

Project 1 from Chapter 8 of the text.  Implement the tax collector program
from figure 8-2 on page 247 of the text.
"""

from breezypythongui import EasyFrame

class TaxCalculatorFrame(EasyFrame):
    def __init__(self):
        """
        Setup widgets on window
        """
        EasyFrame.__init__(self)
        self.addLabel(text="Gross Income",
                      row=0,
                      column=0,
                      sticky="NSEW"
                      )
        self.income = self.addFloatField\
                          (value=0.0,
                           row = 0,
                           column = 1,
                           precision=2
                           )

        self.addLabel(text="Dependencies",
                      row=1,
                      column=0,
                      sticky="NSEW"
                      )
        self.dependencies = self.addIntegerField \
            (value=0,
             row = 1,
             column = 2
             )
        self.addLabel(text="Total Tax",
                      row=3,
                      column=0,
                      sticky="NSEW"
                      )
        self.tax = self.addFloatField \
            (value=0.0,
             row = 3,
             column = 1,
             precision=2,
             state="readonly"
             )

        self.addButton(text = "Compute",
                       row = 2, column = 0,
                       columnspan = 3,
                       command = self.compute
                      )

    # Methods to handle user events.
    def compute(self):
        """
        Calculate tax and update tax box on the screen.
        """
        deps = self.dependencies.getNumber()
        inc  = self.income.getNumber()
        tax  = 0.10 * (inc - 3500.0 * deps)
        tax = tax if tax>0 else 0
        self.tax.setNumber( tax )

def main():
    """ Instantiate window and start gui loop. """
    TaxCalculatorFrame().mainloop()

if __name__ == "__main__":
    main()