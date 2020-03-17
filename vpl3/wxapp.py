#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# server gui with wxPython

from vpl3.baseapp import ApplicationBase
from vpl3.urlutil import URLUtil

import wx
# Ubuntu: sudo apt install python3-wxgtk4.0
# macOS: pip3 install -U wxPython

class QRControl(wx.Control):
    # see implementation of GenStaticText in wx/lib/stattext.py

    def __init__(self, parent, ID=-1,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0,
                 name="QRCode",
                 text=""):
        wx.Control.__init__(self, parent, ID, pos, size, style | wx.NO_BORDER,
                            wx.DefaultValidator, name)
        self.InheritAttributes()
        self.SetInitialSize(size)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: self.OnEraseBackground())

        self.size = size
        self.text = text

    def SetText(self, text):
        self.text = text
        self.Refresh()

    def DoGetBestSize(self):
        return wx.Size(self.size[0], self.size[1])

    def AcceptsFocus(self):
        return False

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)

        width, height = self.GetClientSize()
        backColor = self.GetBackgroundColour()
        dc.SetBackground(wx.Brush(backColor, wx.SOLID))
        dc.Clear()

        import qrcode
        qr = qrcode.QRCode()
        qr.add_data(self.text)
        qr.make()
        n = qr.modules_count
        s = width // (n + 8)  # margin = at least 4 modules
        margin = (width - n * s) / 2
        dc.SetBrush(wx.Brush(wx.BLACK, wx.SOLID))
        for i in range(n):
            for j in range(n):
                if qr.modules[i][j]:
                    dc.DrawRectangle(margin + s * j, margin + s * i, s, s)

    def OnEraseBackground(self):
        pass

class Application(ApplicationBase, wx.App):

    def __init__(self, **kwargs):
        ApplicationBase.__init__(self, **kwargs)
        wx.App.__init__(self)

        size = wx.Size(600, 280)
        self.frame = wx.Frame(None,
                              title=f"{self.tr('VPL Server')} - " + self.tt_url(True),
                              size=size,
                              style=wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER)
        self.frame.SetMaxSize(size)
        self.frame.SetMinSize(size)
        self.frame.Bind(wx.EVT_CLOSE,
                        lambda event: self.quit())

        self.panel = wx.Panel(self.frame)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        self.status = wx.StaticText(self.panel, -1)
        self.vbox.Add(self.status, 0, wx.ALL | wx.EXPAND, 10)

        self.robot_status = wx.StaticText(self.panel, -1)
        self.vbox.Add(self.robot_status, 0, wx.ALL | wx.EXPAND, 10)

        launch_button = wx.Button(self.panel, -1, "Teacher Tools")
        launch_button.Bind(wx.EVT_BUTTON, lambda event: self.start_browser_tt())
        self.vbox.Add(launch_button, 0, wx.CENTER, 10)

        self.qr_code = QRControl(self.panel, size=(160, 160), text="?")
        self.vbox.Add(self.qr_code, 0, wx.CENTER, 10)

        self.vbox.SetSizeHints(self.panel)
        self.panel.SetSizer(self.vbox)

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

        self.update_qr_code()

        self.frame.Show()

    def main_loop(self):
        self.MainLoop()

    def update_qr_code(self):
        path = self.tt_abs_path()
        url = URLUtil.teacher_tools_URL(port=self.http_port,
                                        path=path)
        self.qr_code.SetText(url)

    def show_connection_status(self, str):
        self.status.SetLabel(str)

    def show_robot_status(self, str):
        self.robot_status.SetLabel(str)

    def exit_app(self):
        self.frame.Destroy()
