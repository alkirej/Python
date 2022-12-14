"""
File: savingsaccount.py
This module defines the SavingsAccount class.
"""

class SavingsAccount:
    """This class represents a savings account
    with the owner's name, PIN, and balance."""

    RATE = 0.02    # Single rate for all accounts

    def __init__(self, name, pin, balance = 0.0):
        self.name = name
        self.pin = pin
        self.balance = balance

    def __str__(self):
        """Returns the string rep."""
        result =  'Name:    ' + self.name + '\n' 
        result += 'PIN:     ' + self.pin + '\n' 
        result += 'Balance: ' + str(self.balance)
        return result

    def getBalance(self):
        """Returns the current balance."""
        return self.balance

    def getName(self):
        """Returns the current name."""
        return self.name

    def getPin(self):
        """Returns the current pin."""
        return self.pin

    def deposit(self, amount):
        """If the amount is valid, adds it
        to the balance and returns None;
        otherwise, returns an error message."""
        self.balance += amount
        return None

    def withdraw(self, amount):
        """If the amount is valid, sunstract it
        from the balance and returns None;
        otherwise, returns an error message."""
        if amount < 0:
            return "Amount must be >= 0"
        elif self.balance < amount:
            return "Insufficient funds"
        else:
            self.balance -= amount
            return None

    def computeInterest(self):
        """Computes, deposits, and returns the interest."""
        interest = self.balance * SavingsAccount.RATE
        self.deposit(interest)
        return interest

    def __eq__(self, other):
        """
        Compare 2 accounts.  Accounts are the same if they have the same
        user name and pin (which subs in for an account #)
        """
        return( self.name == other.name and self.pin == other.pin)

    def __lt__(self, other):
        """Compare 2 accounts"""
        if self.name == other.name:
            return self.pin < other.pin
        else:
            return self.name < other.name

    def __ge__(self, other):
        """Compare 2 accounts"""
        if self.name >= other.name:
            return self.pin >= other.pin
        else:
            return self.name >= other.name
