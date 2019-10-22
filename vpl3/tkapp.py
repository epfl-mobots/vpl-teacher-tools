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

        self.title("VPL Server - " + self.address)
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

        # menu
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar)
        file_menu.add_command(label="Open in Browser",
                              command=self.start_browser,
                              accelerator="Meta-B")
        self.bind("<Command-b>", lambda event: self.start_browser())
        self.bind("<Control-q>", lambda event: self.quit())
        menubar.add_cascade(label="File", menu=file_menu)

    def writeln(self, str):
        self.log.insert("end", str + "\n")
        self.log.see(tk.END)

    def show_connection_status(self, str):
        self.ws_info_label["text"] = str

    def main_loop(self):
        self.mainloop()

    def exit_app(self):
        self.destroy()
