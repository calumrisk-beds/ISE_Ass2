from tkinter import *
from Shared_Power.GUI.welcome import Welcome


class Main:
    def __init__(self, master):
        self.master = master
        Welcome(self.master)


if __name__ == "__main__":
    root = Tk()
    Main(root)
    root.mainloop()
