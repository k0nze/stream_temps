try:
    import Tkinter as Tk
except ModuleNotFoundError:
    import tkinter as Tk

import threading
import socketserver
import time

try:
    import Adafruit_DHT
except:
    pass

from pathlib import Path

from .consts import *

from .view import View
from .model import Model
from .web_server import WebServer
from .is_raspberry_pi import is_raspberry_pi


class Controller:
    def __init__(self):
        user_dir = Path.home()
        json_path = Path.joinpath(user_dir, '.stream_temps.json')

        self.is_raspberry_pi = is_raspberry_pi()

        self.model = Model(json_path)

        self.root = Tk.Tk()
        self.view = View(self.model, self)

    def run(self):

        webserver_thread = threading.Thread(target=self.start_webserver)

        # set as deamon such that the thread is killed when the main thread is killed
        webserver_thread.setDaemon(True) 
        webserver_thread.start()

        dht_reader_thread = threading.Thread(target=self.start_dht_reader)

        # set as deamon such that the thread is killed when the main thread is killed
        dht_reader_thread.setDaemon(True) 
        dht_reader_thread.start()

        self.root.title("Stream Temps")
        self.root.deiconify()
        self.root.mainloop()

    def start_webserver(self):
        with socketserver.TCPServer(("", PORT), WebServer) as httpd:
            httpd.serve_forever()

    def start_dht_reader(self):
        if self.is_raspberry_pi:
            DHT_SENSOR = Adafruit_DHT.DHT22
            DHT_PIN = 4

            while True:
                humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

                if humidity is not None and temperature is not None:
                    self.model.set_temperature(temperature)
                else:
                    self.model.set_temperature(None)

                time.sleep(30)

        else:
            while True:
                self.model.set_temperature(42)
                time.sleep(30)

    def quit(self):
        self.root.quit()

    def save_settings(self):
        None
