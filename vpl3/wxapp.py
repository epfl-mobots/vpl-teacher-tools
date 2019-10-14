#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# server gui with wxPython

from vpl3.server import Server
from vpl3.urlutil import URLUtil
from vpl3.db import Db

import threading

import wx  # Ubuntu: sudo apt install python3-wxgtk4.0


class Application(wx.App):

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

        self.frame = wx.Frame(None,
                              title=f"VPL Server - {URLUtil.get_local_IP()}:{self.http_port}",
                              size=wx.Size(800, 500))
        self.frame.Bind(wx.EVT_CLOSE, self.quit)
        self.frame.Show()

        panel = wx.Panel(self.frame)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.ws_info_label = wx.StaticText(panel, -1)
        vbox.Add(self.ws_info_label, 0, wx.ALL | wx.EXPAND, 5)

        self.log = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.log, 1, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(vbox)

        self.update_connection()

        # menu
        file_menu = wx.Menu()
        open_in_browser_item = file_menu.Append(-1, "Open in Browser\tCtrl-B",
                                                "Open VPL3 teacher tools in browser")
        exit_item = file_menu.Append(wx.ID_EXIT)

        menubar = wx.MenuBar()
        menubar.Append(file_menu, "File")
        self.frame.SetMenuBar(menubar)
        self.frame.Bind(wx.EVT_MENU, self.start_browser, open_in_browser_item)
        self.frame.Bind(wx.EVT_MENU, self.quit, exit_item)

    def mainloop(self):
        self.MainLoop()

    def logger(self, str):
        def write():
            self.log.AppendText(str + "\n")
            self.log.PageDown()

        with self.logger_lock:
            wx.CallAfter(write)

    def update_connection(self, session_id=None):
        def update():
            self.ws_info_label.SetLabel(
                f"Number of connections: {self.server.ws_server.connection_count}"
            )

        wx.CallAfter(update)

    def start_browser(self, event=None):
        URLUtil.start_browser(self.http_port, using="chrome")

    def quit(self, event=None):
        self.server.stop()
        self.frame.Destroy()
