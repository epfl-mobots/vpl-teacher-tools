#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# server gui with wxPython

from vpl3.baseapp import ApplicationBase

import wx  # Ubuntu: sudo apt install python3-wxgtk4.0


class Application(ApplicationBase, wx.App):

    def __init__(self, **kwargs):
        ApplicationBase.__init__(self, **kwargs)
        wx.App.__init__(self)

        self.frame = wx.Frame(None,
                              title="VPL Server - " + self.tt_url(True),
                              size=wx.Size(800, 500))
        self.frame.Bind(wx.EVT_CLOSE,
                        lambda event: self.quit())
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
        self.frame.Bind(wx.EVT_MENU,
                        lambda event: self.start_browser_tt(),
                        open_in_browser_item)
        self.frame.Bind(wx.EVT_MENU,
                        lambda event: self.quit(),
                        exit_item)

    def main_loop(self):
        self.MainLoop()

    def writeln(self, str):
        self.log.AppendText(str + "\n")
        self.log.PageDown()

    def show_connection_status(self, str):
        self.ws_info_label.SetLabel(str)

    def exit_app(self):
        self.frame.Destroy()
