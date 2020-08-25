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

import socket

class View(Tk.Frame):
    def __init__(self, model, root):

        self.model = model

        Tk.Frame.__init__(self, root)

        self.pack(fill="both", expand=True)

        menubar = Tk.Menu(self.master)
        self.master.config(menu=menubar)

        
        # file menu
        fileMenu = Tk.Menu(menubar)
        fileMenu.add_command(label="About")
        fileMenu.add_separator()
        fileMenu.add_command(label="Quit", command=root.quit)

        menubar.add_cascade(label="File", menu=fileMenu)

        
        # grid config
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.grid_rowconfigure(1, weight=1)


        # HTML and CSS code editor
        html_label = Tk.Label(self, text="HTML", justify=Tk.LEFT, anchor="w").grid(sticky=Tk.W, row=0, column=0, columnspan=2)
        css_label = Tk.Label(self, text="CSS", justify=Tk.LEFT, anchor="w").grid(sticky=Tk.W, row=0, column=2, columnspan=2)

        self.html_text = ScrolledText(self)
        self.html_text.grid(sticky=Tk.W+Tk.E+Tk.S+Tk.N, row=1, column=0, columnspan=2)
        self.html_text.insert(Tk.END, self.get_html()) 

        self.css_text = ScrolledText(self)
        self.css_text.grid(sticky=Tk.W+Tk.E+Tk.S+Tk.N, row=1, column=2, columnspan=2)
        self.css_text.insert(Tk.END, self.get_css()) 


        # select temperature system
        temperature_system = self.model.get_temperature_system()

        temperature_label = Tk.Label(self, text="Temperature: 36" + temperature_system, justify=Tk.LEFT, anchor="w").grid(sticky=Tk.W, row=2, column=0)

        temperature_system_frame = Tk.Frame(self)
        self.temperature_system_var = Tk.StringVar()
        self.temperature_system_var.set('C')

        temperature_system_c = Tk.Radiobutton(temperature_system_frame, text='C', variable=self.temperature_system_var, value='C')
        temperature_system_c.pack(side=Tk.LEFT)
        temperature_system_c.invoke()

        temperature_system_f = Tk.Radiobutton(temperature_system_frame, text='F', variable=self.temperature_system_var, value='F')
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


    def get_html(self):
        # read root_dir/index.html
        index_html_file = open(ROOT_DIR + "/index.html", "r")
        index_html = index_html_file.read()
        index_html_file.close()
        
        # remove wrapper
        wrapper_index_html_file = open(TEMPLATES_DIR + "/wrapper_index.html", "r")
        wrapper_index_html = wrapper_index_html_file.read().split("$(CONTENT)")
        wrapper_index_html_file.close()

        wrapper_index_html_top = wrapper_index_html[0]
        wrapper_index_html_bottom = wrapper_index_html[1]

        index_html = index_html.replace(wrapper_index_html_top, '') 
        index_html = index_html.replace(wrapper_index_html_bottom, '') 

        return index_html


    def get_css(self):
        # read root_dir/style.css
        style_css_file = open(ROOT_DIR + "/style.css", "r")
        style_css = style_css_file.read()
        style_css_file.close()

        # remove wrapper
        wrapper_style_css_file = open(TEMPLATES_DIR + "/wrapper_style.css", "r")
        wrapper_style_css = wrapper_style_css_file.read().replace("\n$(CONTENT)", "")
        wrapper_style_css_file.close()

        style_css = style_css.replace(wrapper_style_css, "")

        return style_css


    def on_reset(self):
        print("reset")


    def on_apply(self):
        # get scrolled text contents
        html = self.html_text.get("1.0", Tk.END)
        css = self.css_text.get("1.0", Tk.END)

        # apply wrappers
        wrapper_index_html_file = open(TEMPLATES_DIR + "/wrapper_index.html", "r")
        wrapper_index_html = wrapper_index_html_file.read()
        wrapper_index_html_file.close()

        index_html = wrapper_index_html.replace("$(CONTENT)\n", html)

        wrapper_style_css_file = open(TEMPLATES_DIR + "/wrapper_style.css", "r")
        wrapper_style_css = wrapper_style_css_file.read()
        wrapper_style_css_file.close()

        style_css = wrapper_style_css.replace("$(CONTENT)", css.rstrip())

        # write files
        with open(ROOT_DIR + "/index.html", "w") as index_html_file:
            index_html_file.write(index_html)

        with open(ROOT_DIR + "/style.css", "w") as style_css_file:
            style_css_file.write(style_css)
