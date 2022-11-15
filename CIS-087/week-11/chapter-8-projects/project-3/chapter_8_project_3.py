"""
Author: Jeff Alkire
Date:   Nov 10, 2022

Project 3 from Chapter 8 of the text.  Implement Project 4 from chapter 3
(page 99) using a GUI interface.

Convert between degrees centigrade and fahrenheit in both directions using a GUI.
"""

from breezypythongui import EasyFrame

# Temp ration fahrenheit to celsius.
#  Boiling point = 212f 100c
#  Freezing point = 32f 0c
RATIO = (212-32)/(100-0)

class TempFrame(EasyFrame):
    def __init__(self):
        """
        Setup widgets on window
        """
        EasyFrame.__init__(self)
        self.addLabel(text="Centigrade:",
                      row=0,
                      column=0,
                      sticky="NW"
                      )
        self.degrees_c = self.addFloatField \
            (value=0,
             row = 0,
             column = 1,
             precision = 1,
             sticky = "NW"
             )

        self.addLabel(text="Fahrenheit:",
                      row=2,
                      column=0,
                      sticky="NW"
                      )
        self.degrees_f = self.addFloatField \
            (value=0.5,
             row = 2,
             column = 1,
             precision = 1,
             sticky = "NW"
             )

        self.addButton(text = "<<<<",
                       row = 4, column = 0,
                       command = self.to_centigrade
                       )

        self.addButton(text = ">>>>",
                       row = 4, column = 1,
                       command = self.to_fahrenheit
                       )

    # Methods to handle user events.
    def to_centigrade(self):
        """
        Get the degrees fahrenheit, convert to centigrade, and update
        the screen.
        """
        temp = self.degrees_f.getNumber()
        new_temp = (temp-32) / RATIO
        self.degrees_c.setNumber(new_temp)

    def to_fahrenheit(self):
        """
        Get the degrees centigrade, convert to fahrenheit, and update
        the screen.
        """
        temp = self.degrees_c.getNumber()
        new_temp = temp * RATIO + 32
        self.degrees_f.setNumber(new_temp)

def main():
    """ Instantiate window and start gui loop. """
    TempFrame().mainloop()

if __name__ == "__main__":
    main()