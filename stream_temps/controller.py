try:
    import Tkinter as Tk
except ModuleNotFoundError:
    import tkinter as Tk

import threading
import socketserver

from pathlib import Path

from .consts import *

from .view import View
from .model import Model
from .web_server import WebServer


class Controller:
    def __init__(self):
        user_dir = Path.home()
        json_path = Path.joinpath(user_dir, '.stream_temps.json')

        self.model = Model(json_path)

        self.root = Tk.Tk()
        self.view = View(self.model, self)

    def run(self):

        t = threading.Thread(target=self.start_webserver)

        # set as deamon such that the thread is killed when the main thread is killed
        t.setDaemon(True) 
        t.start()

        self.root.title("Stream Temps")
        self.root.deiconify()
        self.root.mainloop()

    def start_webserver(self):
        with socketserver.TCPServer(("", PORT), WebServer) as httpd:
            httpd.serve_forever()

    def quit(self):
        self.root.quit()

    def save_settings(self):
        None
