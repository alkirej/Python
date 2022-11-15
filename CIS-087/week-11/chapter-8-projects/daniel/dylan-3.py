"""
File: temperatureconverter.py
Project 8.3
Author: Dylan Williams

Temperature conversion method between Fahrenheit and Celsius.
Demonstrates the use of numeric data fields.
"""

from breezypythongui import EasyFrame

class TemperatureConverter(EasyFrame):
    """A temperature unit conversion program."""

    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, title = "Temperature Converter")

        # Label and field for Celsius
        self.addLabel(text = "Celsius", row = 0,
                      column = 0)
        self.celsiusField = self.addFloatField(value = 0.0, row = 1,
                                               column = 0, precision = 2)

        # Label and field for Fahrenheit
        self.addLabel(text = "Fahrenheit", row = 0,
                      column = 1)
        self.fahrField = self.addFloatField(value = 32.0, row = 1,
                                            column = 1, precision = 2)

        # Celsius to Fahrenheit conversion button
        self.addButton(text = ">>>>", row = 2,
                       column = 0, command = self.computeFahr)

        # Fahrenheit to Celsius conversion button
        self.addButton(text = "<<<<", row = 2,
                       column = 1, command = self.computeCelsius)

    # The controller methods
    def computeFahr(self):
        """Inputs the Celsius degrees and outputs the
        Fahrenheit degrees."""
        degrees = self.celsiusField.getNumber()
        degrees = degrees * 9 /  5 + 32
        self.fahrField.setNumber(degrees)

    def computeCelsius(self):
        """Inputs the Fahrenheit degrees and outputs the Celsius degrees."""
        degrees =  self.fahrField.getNumber()
        degrees = (degrees - 32) * 5 / 9
        self.celsiusField.setNumber(degrees)

def main():
    """Instantiate and bring up the window."""
    TemperatureConverter().mainloop()

if __name__ == "__main__":
    main()
