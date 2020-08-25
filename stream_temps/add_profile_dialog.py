try:
    import Tkinter as Tk
except ModuleNotFoundError:
    import tkinter as Tk

class AddProfileDialog(Tk.Toplevel):
    def __init__(self, master, model):
        Tk.Toplevel.__init__(self, master)

        self.model = model

        #self.minsize(282, 390)
        #self.resizable(False, False)

        # Label
        # Entry
        # OK Button
        # Cancel Button

