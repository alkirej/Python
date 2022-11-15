"""
File: taxformwithgui.py
Project 8.1
Author: Dylan Williams

A GUI-based tax calculator program.

Calculates and prints the total tax, given the income and number of dependents
(inputs) by the user, and a standard deduction of $10,000, an exemption amount of
$3,000, and a flat tax rate of 20%.
"""

from breezypythongui import EasyFrame

class TaxCalculator(EasyFrame):
    """Application window for using the tax calculator."""

    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, title = "Tax Calculator")

        # Name and field for the income
        self.addLabel(text = "Gross income",
                      row = 0, column = 0)
        self.incomeField = self.addFloatField(value = 0.0, row = 0,
                                              column = 1)

        # Name and field for the total number of dependents
        self.addLabel(text = "Dependents", row = 1,
                      column = 0)
        self.depField = self.addIntegerField(value = 0, row = 1,
                                             column = 1)

        # The command button
        self.addButton(text = "Compute", row = 2, column = 0,
                       columnspan = 2, command = self.computeTax)

        # Name and field for the tax
        self.addLabel(text = "Total Tax", row = 3,
                      column = 0)
        self.taxField = self.addFloatField(value = 0.0, row = 3,
                                           column = 1,
                                           precision = 2,
                                           state = "readonly")

    # The event handler method for the command button
    def computeTax(self):
        """Obtains the data from the input field and utilizes them to
        calculate the tax, which is then sent to the output field."""
        income = self.incomeField.getNumber()
        numDependents = self.depField.getNumber()
        exemptionAmount = 3000.0
        standardDeduction = 10000.0
        tax = (income - numDependents * exemptionAmount - standardDeduction) * .20
        self.taxField.setNumber(max(tax, 0))

def main():
    TaxCalculator().mainloop()

if __name__ == "__main__":
    main()
                      
                       