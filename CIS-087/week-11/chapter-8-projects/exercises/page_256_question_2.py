from breezypythongui import EasyFrame
from tkinter.font import Font

class ImageDemo(EasyFrame):
    """Displays an image and a caption."""

    def __init__(self):
        """Sets up the window and widgets."""
        EasyFrame.__init__(self, title = "Chapter 8 Exercise 2")

        # Rasa text label
        textLabel = self.addLabel(text = "Rasa",
                                  row = 0, column = 0,
                                  sticky = "NSEW")
        font = Font(family = "Courier", size = 20)
        textLabel["font"] = font
        textLabel["foreground"] = "black"

        # FreeSerif text label
        textLabel = self.addLabel(text = "FreeSerif",
                                  row = 0, column = 1,
                                  sticky = "NSEW")
        font = Font(family = "FreeSerif", size = 20)
        textLabel["font"] = font
        textLabel["foreground"] = "blue"

        # FreeSans text label
        textLabel = self.addLabel(text = "FreeSans",
                                  row = 0, column = 2,
                                  sticky = "NSEW")
        font = Font(family = "FreeSans", size = 20)
        textLabel["font"] = font
        textLabel["foreground"] = "purple"

def main():
    """Instantiates and pops up the window."""
    ImageDemo().mainloop()

if __name__ == "__main__":
    main()
