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

        name_label = Tk.Label(self, text="New Profile Name:")
        name_label.grid(sticky=Tk.W, column=0, row=0)

        self.name_variable = Tk.StringVar()
        self.name_variable.set("New Profile")

        name_entry = Tk.Entry(self, width=30, textvariable=self.name_variable)
        name_entry.grid(sticky=Tk.W, column=0, row=1)

        ok_cancel_button_frame = Tk.Frame(self)

        ok_button = Tk.Button(ok_cancel_button_frame, text="OK", command=self.on_ok).pack(side=Tk.LEFT)
        ok_button = Tk.Button(ok_cancel_button_frame, text="Cancel", command=self.on_cancel).pack(side=Tk.LEFT)

        ok_cancel_button_frame.grid(column=0, row=2, sticky=Tk.E+Tk.S)

    def on_ok(self):
        None

    def on_cancel(self):
        None

