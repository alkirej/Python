from breezypythongui import EasyFrame
from tkinter.font import Font

class NineLabelsFrame(EasyFrame):
    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, title = "Chapter 8 Page 259 Exercise 3")

        for row in range(3):
            for col in range(3):
                txt = "(" + str(col) + "," + str(row) + ")"

                self.addLabel(text = txt,
                              row = row,
                              column = col,
                              sticky = "NSEW"
                             )
def main():
    """Instantiates and pops up the window."""
    NineLabelsFrame().mainloop()

if __name__ == "__main__":
    main()
