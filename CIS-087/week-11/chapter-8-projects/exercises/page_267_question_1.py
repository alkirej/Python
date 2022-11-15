from breezypythongui import EasyFrame

class FloatFieldFrame(EasyFrame):
    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, title = "Chapter 8 Page 267 Exercise 1")

        self.addFloatField(value=0.0,
                           row = 1,
                           column = 1,
                           precision=2
                           )

def main():
    """Instantiates and pops up the window."""
    FloatFieldFrame().mainloop()

if __name__ == "__main__":
    main()
