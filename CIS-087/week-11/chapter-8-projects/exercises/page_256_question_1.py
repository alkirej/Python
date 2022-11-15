from breezypythongui import EasyFrame

class PatrioticLabels(EasyFrame):
    """ Display a greeting in  a window. """

    def __init__(self):
        """ Sets up the window and the label. """
        EasyFrame.__init__(self)
        self["background"]="green"
        self.addLabel(text="RED",
                      row=0,
                      column=0,
                      sticky="NSEW",
                      foreground="red",
                      background="green"
                     )
        self.addLabel(text="WHITE",
                      row=1,
                      column=0,
                      sticky="NSEW",
                      foreground="white",
                      background="green"
                     )
        self.addLabel(text="BLUE",
                      row=2,
                      column=0,
                      sticky="NSEW",
                      foreground="blue",
                      background="green"
                     )

def main():
    """ Instantiate and pop up window """
    PatrioticLabels().mainloop()

if __name__ == "__main__":
    main()