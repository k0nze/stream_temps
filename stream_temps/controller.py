try:
    import Tkinter as Tk
except ModuleNotFoundError:
    import tkinter as Tk

from .view import View

class Controller:
    def __init__(self):
        self.root = Tk.Tk()
        self.view = View(self.root)

    def run(self):
        self.root.title("Stream Temps")
        self.root.deiconify()
        self.root.mainloop()

    def quit(self):
        self.root.quit()

    def save_settings(self):
        None
