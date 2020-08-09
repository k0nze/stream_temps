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
DIRECTORY = str(os.path.dirname(os.path.realpath(__file__))) + "/root_dir"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)


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

    html_text = ScrolledText(root).grid(sticky=Tk.W+Tk.E+Tk.S+Tk.N, row=1, column=0, columnspan=2)
    css_text = ScrolledText(root).grid(sticky=Tk.W+Tk.E+Tk.S+Tk.N, row=1, column=2, columnspan=2)

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
    

if __name__ == '__main__':
    run()
