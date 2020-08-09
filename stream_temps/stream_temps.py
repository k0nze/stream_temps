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


import http.server
import socketserver
import threading
import os

PORT = 8000
ROOT_DIR = str(os.path.dirname(os.path.realpath(__file__))) + "/root_dir"
TEMPLATES_DIR = str(os.path.dirname(os.path.realpath(__file__))) + "/templates"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT_DIR, **kwargs)


def start_webserver():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()


def run():

    t = threading.Thread(target=start_webserver)

    # set as deamon such that the thread is killed when the main thread is killed
    t.setDaemon(True) 
    t.start()

    root = Tk.Tk()
    root.title("Stream Temps")
    root.deiconify()

    menubar = Tk.Menu(root)
    root.config(menu=menubar)

    fileMenu = Tk.Menu(menubar)
    fileMenu.add_command(label="About")
    fileMenu.add_separator()
    fileMenu.add_command(label="Quit", command=root.quit)

    menubar.add_cascade(label="File", menu=fileMenu)


    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_columnconfigure(3, weight=1)

    root.grid_rowconfigure(1, weight=1)


    html_label = Tk.Label(root, text="HTML", justify=Tk.LEFT, anchor="w").grid(sticky=Tk.W, row=0, column=0, columnspan=2)
    css_label = Tk.Label(root, text="CSS", justify=Tk.LEFT, anchor="w").grid(sticky=Tk.W, row=0, column=2, columnspan=2)

    html_text = ScrolledText(root)
    html_text.grid(sticky=Tk.W+Tk.E+Tk.S+Tk.N, row=1, column=0, columnspan=2)
    html_text.insert(Tk.END, get_html()) 

    css_text = ScrolledText(root)
    css_text.grid(sticky=Tk.W+Tk.E+Tk.S+Tk.N, row=1, column=2, columnspan=2)
    css_text.insert(Tk.END, get_css()) 

    temperature_label = Tk.Label(root, text="Temperature: 36C", justify=Tk.LEFT, anchor="w").grid(sticky=Tk.W, row=2, column=0)

    temperature_system_frame = Tk.Frame(root)
    temperature_system_var = Tk.StringVar()
    temperature_system_var.set("C")

    temperature_system_c = Tk.Radiobutton(temperature_system_frame, text="C", variable=temperature_system_var, value="C").pack(side=Tk.LEFT)
    temperature_system_f = Tk.Radiobutton(temperature_system_frame, text="F", variable=temperature_system_var, value="F").pack(side=Tk.LEFT)
 
    temperature_system_frame.grid(sticky=Tk.E, row=2, column=1)
    
    reset_apply_button_frame = Tk.Frame(root)

    reset_button = Tk.Button(reset_apply_button_frame, text="Reset").pack(side=Tk.LEFT)
    apply_button = Tk.Button(reset_apply_button_frame, text="Apply").pack(side=Tk.LEFT)

    reset_apply_button_frame.grid(row=2, column=2, columnspan=2, sticky=Tk.E+Tk.S)

    root.mainloop()


def get_html():
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


def get_css():
    # read root_dir/style.css
    style_css_file = open(ROOT_DIR + "/style.css", "r")
    style_css = style_css_file.read()
    style_css_file.close()

    # remove wrapper
    wrapper_style_css_file = open(TEMPLATES_DIR + "/wrapper_style.css", "r")
    wrapper_style_css = wrapper_style_css_file.read().replace("$(CONTENT)", "")
    wrapper_style_css_file.close()

    print(wrapper_style_css)

    style_css = style_css.replace(wrapper_style_css, "")

    return style_css



if __name__ == '__main__':
    run()
