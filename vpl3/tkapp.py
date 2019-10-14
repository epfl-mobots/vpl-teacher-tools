#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# server gui with tkinter

from vpl3.server import Server
from vpl3.db import Db
from vpl3.urlutil import URLUtil

import threading

import tkinter as tk
from tkinter.scrolledtext import ScrolledText


class Application(tk.Tk):

    DEFAULT_HTTP_PORT = Server.DEFAULT_HTTP_PORT
    DEFAULT_WS_PORT = Server.DEFAULT_WS_PORT

    def __init__(self,
                 db_path=Db.DEFAULT_PATH,
                 http_port=DEFAULT_HTTP_PORT,
                 ws_port=DEFAULT_WS_PORT,
                 ws_link_url=None):
        self.http_port = http_port
        self.logger_lock = threading.Lock()
        self.server = Server(db_path=db_path,
                             http_port=http_port,
                             ws_port=ws_port,
                             ws_link_url=ws_link_url,
                             logger=self.logger,
                             update_connection=self.update_connection)
        self.server.start()

        super().__init__()
        self.title(f"VPL Server - {URLUtil.get_local_IP()}:{self.http_port}")
        self.protocol("WM_DELETE_WINDOW", self.quit)  # close widget
        self.createcommand("exit", self.quit)  # Quit menu
        self.grid()
        tk.Grid.columnconfigure(self, 0, weight=1)

        # self.browser_button = tk.Button(self, text="Teacher Tools",
        #                                 command=self.start_browser)
        # self.browser_button.grid()

        self.ws_info_label = tk.Label(self)
        self.ws_info_label.grid(sticky=tk.W)

        self.log = ScrolledText(self)
        self.log.grid(sticky=tk.N+tk.W+tk.E+tk.S)

        self.update_connection()

        # menu
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar)
        file_menu.add_command(label="Open in Browser",
                              command=self.start_browser,
                              accelerator="Meta-B")
        self.bind("<Command-b>", self.start_browser)
        self.bind("<Control-b>", self.start_browser)
        menubar.add_cascade(label="File", menu=file_menu)

    def logger(self, str):
        with self.logger_lock:
            self.log.insert("end", str + "\n")
            self.log.see(tk.END)

    def update_connection(self, session_id=None):
        self.ws_info_label["text"] = \
            f"Number of connections: {self.server.ws_server.connection_count}"

    def start_browser(self, event=None):
        URLUtil.start_browser(self.http_port, using="chrome")

    def quit(self):
        self.server.stop()
        self.destroy()
