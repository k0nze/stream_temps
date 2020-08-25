try:
    import Tkinter as Tk
    from Tkinter import ttk
except ModuleNotFoundError:
    import tkinter as Tk
    from tkinter import ttk

from .main_window import MainWindow


class View:
    def __init__(self, model, controller):

        self.controller = controller 
        self.model = model

        self.main_window = MainWindow(self.model, self.controller.root)
