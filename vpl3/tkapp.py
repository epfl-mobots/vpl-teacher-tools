#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# server gui with tkinter

from vpl3.baseapp import ApplicationBase

import tkinter as tk
from tkinter.scrolledtext import ScrolledText


class Application(ApplicationBase, tk.Tk):

    def __init__(self, **kwargs):
        ApplicationBase.__init__(self, **kwargs)
        tk.Tk.__init__(self)

        self.shorten_url = False

        self.title("VPL Server - " + self.address)
        self.protocol("WM_DELETE_WINDOW", self.quit)  # close widget
        self.createcommand("exit", self.quit)  # Quit menu
        self.grid()
        tk.Grid.columnconfigure(self, 0, weight=1)

        # self.browser_button = tk.Button(self, text="Teacher Tools",
        #                                 command=self.start_browser_tt)
        # self.browser_button.grid()

        self.ws_info_label = tk.Label(self)
        self.ws_info_label.grid(sticky=tk.W)

        self.log = ScrolledText(self)
        self.log.grid(sticky=tk.N+tk.W+tk.E+tk.S)

        # menus
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="Open in Browser",
                              command=self.start_browser_tt,
                              accelerator="Control-B")
        self.bind("<Control-b>", lambda event: self.start_browser_tt())
        self.bind("<Control-q>", lambda event: self.quit())
        menubar.add_cascade(label="File", menu=file_menu)
        options_menu = tk.Menu(menubar, tearoff=False)
        self.v_shorten_url = tk.BooleanVar(value=True)
        self.v_shorten_url.trace("w",
                                 lambda name, i, op:
                                 self.menu_item_shorten_urls(self.v_shorten_url.get()))
        self.v_language = tk.StringVar(value="fr")
        options_menu.add_checkbutton(label="Shorten URLs",
                                     variable=self.v_shorten_url)
        options_menu.add_separator()
        options_menu.add_radiobutton(label="English",
                                     variable=self.v_language,
                                     value="en",
                                     command=lambda: self.set_language("en"))
        options_menu.add_radiobutton(label="French",
                                     variable=self.v_language,
                                     value="fr",
                                     command=lambda: self.set_language("fr"))
        menubar.add_cascade(label="Options", menu=options_menu)

    def writeln(self, str):
        self.log.insert("end", str + "\n")
        self.log.see(tk.END)

    def show_connection_status(self, str):
        self.ws_info_label["text"] = str

    def menu_item_shorten_urls(self, b):
        self.shorten_url = b
        self.server.http_server.full_url = not self.shorten_url

    def main_loop(self):
        self.mainloop()

    def exit_app(self):
        self.destroy()
