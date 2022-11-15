from breezypythongui import EasyFrame

class IntegerFieldFrame(EasyFrame):
    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, title = "Chapter 8 Page 267 Exercise 3")

        self.num_value = self.addIntegerField\
                          (value=0,
                           row = 0,
                           column = 0
                           )

        self.button = self.addButton \
                                (text="Check #",
                                 row=1,
                                 column=0,
                                 command = self.do_work
                                )
    def do_work(self):
        x = self.num_value.getNumber()
        x *= 10
        self.num_value.setNumber(x)

def main():
    """Instantiates and pops up the window."""
    IntegerFieldFrame().mainloop()

if __name__ == "__main__":
    main()
