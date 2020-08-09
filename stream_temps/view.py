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

class View(Tk.Frame):
    def __init__(self, root):
        Tk.Frame.__init__(self, root)

        self.pack(fill="both", expand=True)

        menubar = Tk.Menu(self.master)
        self.master.config(menu=menubar)


        fileMenu = Tk.Menu(menubar)
        fileMenu.add_command(label="About")
        fileMenu.add_separator()
        fileMenu.add_command(label="Quit", command=root.quit)

        menubar.add_cascade(label="File", menu=fileMenu)


        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.grid_rowconfigure(1, weight=1)


        html_label = Tk.Label(self, text="HTML", justify=Tk.LEFT, anchor="w").grid(sticky=Tk.W, row=0, column=0, columnspan=2)
        css_label = Tk.Label(self, text="CSS", justify=Tk.LEFT, anchor="w").grid(sticky=Tk.W, row=0, column=2, columnspan=2)

        html_text = ScrolledText(self)
        html_text.grid(sticky=Tk.W+Tk.E+Tk.S+Tk.N, row=1, column=0, columnspan=2)
        html_text.insert(Tk.END, self.get_html()) 

        css_text = ScrolledText(self)
        css_text.grid(sticky=Tk.W+Tk.E+Tk.S+Tk.N, row=1, column=2, columnspan=2)
        css_text.insert(Tk.END, self.get_css()) 

        temperature_label = Tk.Label(self, text="Temperature: 36C", justify=Tk.LEFT, anchor="w").grid(sticky=Tk.W, row=2, column=0)

        temperature_system_frame = Tk.Frame(self)
        temperature_system_var = Tk.StringVar()
        temperature_system_var.set("C")

        temperature_system_c = Tk.Radiobutton(temperature_system_frame, text="C", variable=temperature_system_var, value="C").pack(side=Tk.LEFT)
        temperature_system_f = Tk.Radiobutton(temperature_system_frame, text="F", variable=temperature_system_var, value="F").pack(side=Tk.LEFT)
     
        temperature_system_frame.grid(sticky=Tk.E, row=2, column=1)
        
        reset_apply_button_frame = Tk.Frame(self)

        reset_button = Tk.Button(reset_apply_button_frame, text="Reset").pack(side=Tk.LEFT)
        apply_button = Tk.Button(reset_apply_button_frame, text="Apply").pack(side=Tk.LEFT)

        reset_apply_button_frame.grid(row=2, column=2, columnspan=2, sticky=Tk.E+Tk.S)


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
        wrapper_style_css = wrapper_style_css_file.read().replace("$(CONTENT)", "")
        wrapper_style_css_file.close()

        style_css = style_css.replace(wrapper_style_css, "")

        return style_css


        
