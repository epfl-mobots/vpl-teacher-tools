#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# server gui with tkinter

from vpl3.baseapp import ApplicationBase
from vpl3.urlutil import URLUtil

import tkinter as tk
from tkinter.scrolledtext import ScrolledText


class Application(ApplicationBase, tk.Tk):

    def __init__(self, **kwargs):
        ApplicationBase.__init__(self, **kwargs)
        tk.Tk.__init__(self)

        self.shorten_url = False
        self.login_qr_code = False
        self.log_in_dashboard = False

        self.title("VPL Server - " + self.tt_url(True))
        self.protocol("WM_DELETE_WINDOW", self.quit)  # close widget
        self.createcommand("exit", self.quit)  # Quit menu

        padding = 10

        self.status = tk.Label(self, anchor=tk.W, width=30)
        self.status.pack(padx=padding, pady=padding)

        self.robot_status = tk.Label(self, anchor=tk.W, width=30)
        self.robot_status.pack(padx=padding, pady=padding)

        self.browser_button = tk.Button(self, text="Teacher Tools",
                                        command=self.start_browser_tt)
        self.browser_button.pack(padx=padding, pady=padding)

        self.qr_canvas = tk.Canvas(width=160, height=160)
        self.qr_canvas.pack(padx=padding, pady=padding)
        self.draw_qr_code()

        #self.log = ScrolledText(self)
        #self.log.grid(sticky=tk.N+tk.W+tk.E+tk.S)
        self.log = None

        # menus
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        self.file_menu = tk.Menu(menubar, tearoff=False)
        self.file_menu.add_command(label="Open in Browser",
                                   command=self.start_browser_tt,
                                   accelerator="Control-B")
        self.bind("<Control-b>", lambda event: self.start_browser_tt())
        self.bind("<Control-q>", lambda event: self.quit())
        menubar.add_cascade(label="File", menu=self.file_menu)
        self.edit_menu = tk.Menu(menubar, tearoff=False)
        self.edit_menu.add_command(label="Copy URL",
                                   command=self.menu_item_copy_url,
                                   accelerator="Control-C")
        self.bind("<Control-c>", lambda event: self.menu_item_copy_url())
        menubar.add_cascade(label="Edit", menu=self.edit_menu)
        self.options_menu = tk.Menu(menubar, tearoff=False)
        self.v_shorten_url = tk.BooleanVar(value=True)
        self.v_shorten_url.trace("w",
                                 lambda name, i, op:
                                 self.menu_item_shorten_urls(self.v_shorten_url.get()))
        self.v_login_qr_code = tk.BooleanVar(value=False)
        self.v_login_qr_code.trace("w",
                                   lambda name, i, op:
                                   self.menu_item_login_qr_code(self.v_login_qr_code.get()))
        self.v_log_in_dashboard = tk.BooleanVar(value=False)
        self.v_log_in_dashboard.trace("w",
                                      lambda name, i, op:
                                      self.menu_item_log_in_dashboard(self.v_log_in_dashboard.get()))
        self.v_advanced_sim_features = tk.BooleanVar(value=False)
        self.v_advanced_sim_features.trace("w",
                                           lambda name, i, op:
                                           self.menu_item_advanced_sim_features(self.v_advanced_sim_features.get()))
        self.v_dev_tools = tk.BooleanVar(value=False)
        self.v_dev_tools.trace("w",
                               lambda name, i, op:
                               self.menu_item_dev_tools(self.v_dev_tools.get()))
        self.v_language = tk.StringVar(value="fr")
        self.v_bridge = tk.StringVar(value=self.bridge)
        self.options_menu.add_checkbutton(label="Shorten URLs",
                                          variable=self.v_shorten_url)
        self.options_menu.add_checkbutton(label="Login Screen QR Code",
                                          variable=self.v_login_qr_code)
        self.options_menu.add_checkbutton(label="Log Display in Dashboard",
                                          variable=self.v_log_in_dashboard)
        self.options_menu.add_checkbutton(label="Advanced Simulator Features",
                                          variable=self.v_advanced_sim_features)
        self.options_menu.add_checkbutton(label="Developer Tools",
                                          variable=self.v_dev_tools)
        self.options_menu.add_separator()
        
        def change_language(language):
            self.set_language(language)
            self.draw_qr_code()

        self.options_menu.add_radiobutton(label="English",
                                          variable=self.v_language,
                                          value="en",
                                          command=lambda: change_language("en"))
        self.options_menu.add_radiobutton(label="French",
                                          variable=self.v_language,
                                          value="fr",
                                          command=lambda: change_language("fr"))
        self.options_menu.add_separator()
        self.options_menu.add_radiobutton(label="Thymio Device Manager",
                                          variable=self.v_bridge,
                                          value="tdm",
                                          command=lambda: self.menu_item_bridge("tdm"))
        self.options_menu.add_radiobutton(label="JSON WebSocket",
                                          variable=self.v_bridge,
                                          value="jws",
                                          command=lambda: self.menu_item_bridge("jws"))
        self.options_menu.add_radiobutton(label="No Robot",
                                          variable=self.v_bridge,
                                          value="none",
                                          command=lambda: self.menu_item_bridge("none"))
        menubar.add_cascade(label="Options", menu=self.options_menu)

    def disable_serial(self):
        self.no_serial = True
        self.options_menu.entryconfig("JSON WebSocket", state="disabled")

    def writeln(self, str):
        if self.log:
            self.log.insert("end", str + "\n")
            self.log.see(tk.END)

    def show_connection_status(self, str):
        if str:
            self.status["text"] = str

    def show_robot_status(self, str):
        if str:
            self.robot_status["text"] = str

    def draw_qr_code(self):
        import qrcode
        qr = qrcode.QRCode()
        path = self.tt_abs_path()
        url = URLUtil.teacher_tools_URL(port=self.http_port,
                                        path=path)
        qr.add_data(url)
        qr.make()
        n = qr.modules_count
        qr_size = int(self.qr_canvas["width"])
        s = qr_size // (n + 8)  # margin = at least 4 modules
        margin = (qr_size - n * s) / 2
        self.qr_canvas.delete("all")
        for i in range(n):
            for j in range(n):
                if qr.modules[i][j]:
                    self.qr_canvas.create_rectangle(margin + s * j, margin + s * i, margin + s * j + s, margin + s * i + s, fill="#000")

    def menu_item_copy_url(self):
        path = self.tt_abs_path()
        url = URLUtil.teacher_tools_URL(port=self.http_port,
                                        path=path)
        self.clipboard_clear()
        self.clipboard_append(url)

    def menu_item_shorten_urls(self, b):
        self.shorten_url = b
        self.server.http_server.full_url = not self.shorten_url

    def menu_item_login_qr_code(self, b):
        self.login_qr_code = b
        self.server.http_server.has_login_qr_code = self.login_qr_code

    def menu_item_log_in_dashboard(self, b):
        self.log_in_dashboard = b
        self.server.http_server.log_display = self.log_in_dashboard

    def menu_item_advanced_sim_features(self, b):
        self.advanced_sim_features = b
        self.server.http_server.advanced_sim_features = self.advanced_sim_features

    def menu_item_dev_tools(self, b):
        self.dev_tools = b
        self.server.http_server.dev_tools = self.dev_tools

    def menu_item_bridge(self, bridge):
        self.bridge = bridge
        self.server.http_server.bridge = bridge

    def main_loop(self):
        self.mainloop()

    def exit_app(self):
        self.destroy()
