try:
    import Tkinter as Tk
except ModuleNotFoundError:
    import tkinter as Tk

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
        print("serving at port", PORT)
        httpd.serve_forever()


def run():


    t = threading.Thread(target=start_webserver)

    # set as deamon such that the thread is killed when the main thread is killed
    t.setDaemon(True) 
    t.start()

    root = Tk.Tk()
    root.title("Temperature Webserver")
    root.deiconify()
    root.mainloop()

    
if __name__ == '__main__':
    run()
