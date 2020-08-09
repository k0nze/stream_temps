try:
    import Tkinter as Tk
    from Tkinter import ttk
except ModuleNotFoundError:
    import tkinter as Tk
    from tkinter import ttk

class View(Tk.Frame):
    def __init__(self, root):
        Tk.Frame.__init__(self, root)
