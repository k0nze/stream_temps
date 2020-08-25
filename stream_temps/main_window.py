try:
    import Tkinter as Tk
    from Tkinter import ttk
    import Tkinter.font as TkFont
    from Tkinter.scrolledtext import ScrolledText
except ModuleNotFoundError:
    import tkinter as Tk
    from tkinter import ttk
    import tkinter.font as TkFont
    from tkinter.scrolledtext import ScrolledText

from .consts import *
from .add_profile_dialog import AddProfileDialog

import socket
import copy

class MainWindow(Tk.Frame):
    def __init__(self, model, root):

        self.model = model
        self.model.register_observer(self)

        self.root = root

        Tk.Frame.__init__(self, self.root)

        self.pack(fill="both", expand=True)

        self.menubar = Tk.Menu(self.master)
        self.master.config(menu=self.menubar)

        
        # file menu
        file_menu = Tk.Menu(self.menubar)
        file_menu.add_command(label="About", command=self.on_about)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.root.quit)

        self.menubar.add_cascade(label="File", menu=file_menu)

        # profiles menu
        self.update_profiles_menu()
                
        # grid config
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.grid_rowconfigure(1, weight=1)

        self.current_profile = self.model.get_default_profile_name() 

        # HTML and CSS code editor
        html_label = Tk.Label(self, text="HTML", justify=Tk.LEFT, anchor="w").grid(sticky=Tk.W, row=0, column=0, columnspan=2)
        css_label = Tk.Label(self, text="CSS", justify=Tk.LEFT, anchor="w").grid(sticky=Tk.W, row=0, column=2, columnspan=2)

        self.html_text = ScrolledText(self)
        self.html_text.grid(sticky=Tk.W+Tk.E+Tk.S+Tk.N, row=1, column=0, columnspan=2)
        self.html_text.insert(Tk.END, self.model.get_html()) 

        self.css_text = ScrolledText(self)
        self.css_text.grid(sticky=Tk.W+Tk.E+Tk.S+Tk.N, row=1, column=2, columnspan=2)
        self.css_text.insert(Tk.END, self.model.get_css()) 


        # select temperature system
        temperature_system = self.model.get_temperature_system()

        self.temperature_label_var = Tk.StringVar()
        self.temperature_label_var.set(TEMPERATURE_SYSTEM_LABEL_TEXT + temperature_system)
        temperature_label = Tk.Label(self, textvariable=self.temperature_label_var, justify=Tk.LEFT, anchor="w").grid(sticky=Tk.W, row=2, column=0)

        temperature_system_frame = Tk.Frame(self)
        self.temperature_system_var = Tk.StringVar()
        self.temperature_system_var.set(temperature_system)

        temperature_system_c = Tk.Radiobutton(temperature_system_frame, text='C', variable=self.temperature_system_var, value='C', command=self.on_temperature_system_change)
        temperature_system_c.pack(side=Tk.LEFT)

        temperature_system_f = Tk.Radiobutton(temperature_system_frame, text='F', variable=self.temperature_system_var, value='F', command=self.on_temperature_system_change)
        temperature_system_f.pack(side=Tk.LEFT)
     
        temperature_system_frame.grid(sticky=Tk.E, row=2, column=1)

        
        # reset and apply buttons
        reset_apply_button_frame = Tk.Frame(self)

        reset_button = Tk.Button(reset_apply_button_frame, text="Reset", command=self.on_reset).pack(side=Tk.LEFT)
        apply_button = Tk.Button(reset_apply_button_frame, text="Apply", command=self.on_apply).pack(side=Tk.LEFT)

        reset_apply_button_frame.grid(row=2, column=2, columnspan=2, sticky=Tk.E+Tk.S)

        
        # url 
        url_label = Tk.Label(self, text="Browser Source URL:", justify=Tk.LEFT, anchor="w").grid(sticky=Tk.W, row=3, column=0, columnspan=2)

        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)

        url_string_var = Tk.StringVar()
        url_string_var.set("http://"+ip_addr+":"+str(PORT))
        url_entry = Tk.Entry(self, textvariable=url_string_var, state='readonly', justify=Tk.LEFT).grid(sticky=Tk.E+Tk.W, row=4, column=0, columnspan=2)


    def update_profiles_menu(self):
        self.menubar.delete(2)
        profiles_menu = Tk.Menu(self.menubar)

        profile_names = self.model.get_profile_names()

        for profile_name in profile_names:
            profiles_menu.add_command(label=profile_name, command=lambda profile_name=profile_name: self.on_select_profile(profile_name))

        profiles_menu.add_separator()
        profiles_menu.add_command(label="Add New Profile", command=self.on_add_profile)
        profiles_menu.add_command(label="Delete Current Profile", command=self.on_delete_profile)

        self.menubar.add_cascade(label="Profiles", menu=profiles_menu)


    def notify(self):
        self.temperature_label_var.set(TEMPERATURE_SYSTEM_LABEL_TEXT + self.model.get_temperature_system())
        self.update_profiles_menu()


    def on_temperature_system_change(self):
        self.model.set_temperature_system(self.temperature_system_var.get())


    def on_reset(self):
        print("reset")


    def on_apply(self):
        # get scrolled text contents
        html = self.html_text.get("1.0", Tk.END)
        css = self.css_text.get("1.0", Tk.END)

        self.model.save_profile(html, css)

    def on_about(self):
        print("about")
    
    def on_select_profile(self, profile_name):
        self.current_profile = profile_name
        # TODO update html and css

    def on_add_profile(self):
        add_profile_dialog = AddProfileDialog(self.root, self.model)

        # make window modal
        add_profile_dialog.wait_visibility()
        add_profile_dialog.focus_set()
        add_profile_dialog.grab_set()
        add_profile_dialog.transient(self.root)

    def on_delete_profile(self):
        profile_to_delete = self.current_profile
        self.current_profile = self.model.get_default_profile_name() 
        self.model.delete_profile(profile_to_delete)
