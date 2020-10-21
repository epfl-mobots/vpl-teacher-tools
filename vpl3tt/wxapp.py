#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# server gui with wxPython

from vpl3tt.baseapp import ApplicationBase
from vpl3tt.urlutil import URLUtil

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
        self.load_prefs()

        self.frame = wx.Frame(None,
                              title=f"{self.tr('VPL Server')} - " + self.tt_url(True),
                              style=wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER)
        self.frame.Bind(wx.EVT_CLOSE,
                        lambda event: self.quit())
        self.frame.SetMinSize(wx.Size(600, 280))

        self.panel = wx.Panel(self.frame)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        self.status = wx.StaticText(self.panel, -1)
        self.vbox.Add(self.status, 0, wx.ALL | wx.EXPAND, 10)

        self.robot_status = wx.StaticText(self.panel, -1)
        self.vbox.Add(self.robot_status, 0, wx.ALL | wx.EXPAND, 10)

        launch_button = wx.Button(self.panel, -1, "Teacher Tools")
        launch_button.Bind(wx.EVT_BUTTON, lambda event: self.start_browser_tt())
        self.vbox.Add(launch_button, 0, wx.CENTER)

        self.qr_code = QRControl(self.panel, size=(160, 160), text="?")
        self.vbox.Add(self.qr_code, 0, wx.ALL | wx.CENTER, 10)

        self.vbox.SetSizeHints(self.panel)
        self.panel.SetSizerAndFit(self.vbox)
        self.frame.Fit()

        self.update_connection()

        # menu
        menubar = wx.MenuBar()

        file_menu = wx.Menu()
        menubar.Append(file_menu, "File")
        self.menu_item_open_tool = file_menu.Append(-1,
                                                    "Open in Browser\tCtrl-B",
                                                    "Open VPL3 teacher tools in browser")
        self.frame.Bind(wx.EVT_MENU,
                        lambda event: self.start_browser_tt(),
                        self.menu_item_open_tool)
        menu_item = file_menu.Append(wx.ID_EXIT,
                                     "Quit\tCtrl-Q")
        self.frame.Bind(wx.EVT_MENU,
                        lambda event: self.quit(),
                        menu_item)

        edit_menu = wx.Menu()
        menubar.Append(edit_menu, "Edit")
        self.menu_item_copy_url = edit_menu.Append(-1,
                                                   "Copy URL\tCtrl-C",
                                                   "Copy the teacher tool URL to the clipboard")
        self.frame.Bind(wx.EVT_MENU,
                        lambda event: self.do_menu_item_copy_url(),
                        self.menu_item_copy_url)

        options_menu = wx.Menu()
        menubar.Append(options_menu, "Options")
        self.menu_item_shortened_urls = options_menu.AppendCheckItem(-1,
                                                                     "Shortened URLs")
        self.menu_item_shortened_urls.Check(not self.full_url)
        self.frame.Bind(wx.EVT_MENU,
                        lambda event: self.do_menu_item_shortened_urls(),
                        self.menu_item_shortened_urls)
        self.menu_item_login_screen_qr_code = options_menu.AppendCheckItem(-1,
                                                                           "Login Screen QR Code")
        self.menu_item_login_screen_qr_code.Check(self.has_login_qr_code)
        self.frame.Bind(wx.EVT_MENU,
                        lambda event: self.do_menu_item_login_screen_qr_code(),
                        self.menu_item_login_screen_qr_code)
        self.menu_item_log_display = options_menu.AppendCheckItem(-1,
                                                                  "Log Display in Dashboard")
        self.menu_item_log_display.Check(self.log_display)
        self.frame.Bind(wx.EVT_MENU,
                        lambda event: self.do_menu_item_log_display(),
                        self.menu_item_log_display)
        self.menu_item_advanced_sim_features = options_menu.AppendCheckItem(-1,
                                                                           "Advanced Simulator Features")
        self.menu_item_advanced_sim_features.Check(self.advanced_sim_features)
        self.frame.Bind(wx.EVT_MENU,
                        lambda event: self.do_menu_item_advanced_sim_features(),
                        self.menu_item_advanced_sim_features)
        self.menu_item_dev_tools = options_menu.AppendCheckItem(-1,
                                                                "Developer Tools")
        self.menu_item_dev_tools.Check(self.dev_tools)
        self.frame.Bind(wx.EVT_MENU,
                        lambda event: self.do_menu_item_dev_tools(),
                        self.menu_item_dev_tools)

        self.frame.SetMenuBar(menubar)

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

    def do_menu_item_copy_url(self):
        if wx.TheClipboard.Open():
            path = self.tt_abs_path()
            url = URLUtil.teacher_tools_URL(port=self.http_port,
                                            path=path)
            wx.TheClipboard.SetData(wx.TextDataObject(url))
            wx.TheClipboard.Close()

    def do_menu_item_shortened_urls(self):
        self.set_full_url(not self.menu_item_shortened_urls.IsChecked())
        self.save_prefs()

    def do_menu_item_login_screen_qr_code(self):
        self.set_login_qr_code(self.menu_item_login_screen_qr_code.IsChecked())
        self.save_prefs()

    def do_menu_item_log_display(self):
        self.set_log_display(self.menu_item_log_display.IsChecked())
        self.save_prefs()

    def do_menu_item_advanced_sim_features(self):
        self.set_advanced_sim_features(self.menu_item_advanced_sim_features.IsChecked())
        self.save_prefs()

    def do_menu_item_dev_tools(self):
        self.set_dev_tools(self.menu_item_dev_tools.IsChecked())
        self.save_prefs()
