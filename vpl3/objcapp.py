#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# server gui with objc (for macOS only)

from vpl3.baseapp import ApplicationBase
from vpl3.cacaoapp import ApplicationObjCShell
from vpl3.urlutil import URLUtil
from Cocoa import *


class Application(ApplicationBase):

    def __init__(self, **kwargs):
        ApplicationBase.__init__(self, **kwargs)

        self.shorten_url = False
        self.login_qr_code = False
        self.log_display = False
        self.dev_tools = False

        self.app_objc = ApplicationObjCShell.alloc().init()
        self.app_objc.addMenu_withItems_("File", [
            [
                "Open Tools in Browser",
                "b",
                lambda sender: self.start_browser_tt()
            ]
        ])
        self.app_objc.addMenu_withItems_("Edit", [
            [
                "Copy URL",
                "c",
                lambda sender: self.menu_item_copy_url()
            ]
        ])
        self.app_objc.addMenu_withItems_("Options", [
            [
                "Shorten URLs",
                None,
                lambda sender: self.menu_item_shorten_urls()
            ],
            [
                "Login Screen QR Code",
                None,
                lambda sender: self.menu_item_login_QR_code()
            ],
            [
                "Log Display in Dashboard",
                None,
                lambda sender: self.menu_item_log_display()
            ],
            [
                "Developer Tools",
                None,
                lambda sender: self.menu_item_dev_tools()
            ],
            None,
            [
                "English",
                None,
                lambda sender: self.menu_item_language("en")
            ],
            [
                "French",
                None,
                lambda sender: self.menu_item_language("fr")
            ],
            None,
            [
                "Thymio Device Manager",
                None,
                lambda sender: self.menu_item_bridge("tdm")
            ],
            [
                "JSON WebSocket",
                None,
                lambda sender: self.menu_item_bridge("jws")
            ],
            [
                "No Robot",
                None,
                lambda sender: self.menu_item_bridge("none")
            ],
        ])
        self.app_objc.start()
        self.menu_item_shorten_urls()
        self.menu_item_language("fr")
        self.menu_item_bridge("tdm")
        window = self.app_objc.createWindowWithTitle_width_height_x_y_(
            "VPL Server - " + self.tt_url(True),
            400, 120,
            20, 20
        )
        self.status = self.app_objc.addLabelToWindow_title_width_x_y_(window,
                                                                      "",
                                                                      250, 10, 80)
        self.robots_status = self.app_objc.addLabelToWindow_title_width_x_y_(window,
                                                                             "",
                                                                             250, 10, 60)
        self.app_objc.addButtonToWindow_title_action_width_x_y_(window,
                                                                "Open tools in browser",
                                                                lambda sender: self.start_browser_tt(),
                                                                180, 110, 20)

    def disable_serial(self):
        self.no_serial = True
        item = self.app_objc.getMenuItemWithTitle_inMenu_("JSON WebSocket", "Options")
        item.setEnabled_(0)

    def main_loop(self):
        self.app_objc.run()

    def show_connection_status(self, str):
        if self.status:
            self.status.setStringValue_(str)

    def show_robots_status(self, str):
        if self.robots_status:
            self.robots_status.setStringValue_(str)

    def menu_item_copy_url(self):
        path = self.tt_abs_path()
        url = URLUtil.teacher_tools_URL(port=self.http_port,
                                        path=path)
        pasteboard = NSPasteboard.generalPasteboard()
        pasteboard.clearContents()
        pasteboard.setString_forType_(url, NSStringPboardType)

    def menu_item_shorten_urls(self):
        item = self.app_objc.getMenuItemWithTitle_inMenu_("Shorten URLs", "Options")
        self.shorten_url = not self.shorten_url
        item.setState_(1 if self.shorten_url else 0)
        self.server.http_server.full_url = not self.shorten_url

    def menu_item_login_QR_code(self):
        item = self.app_objc.getMenuItemWithTitle_inMenu_("Login Screen QR Code", "Options")
        self.login_qr_code = not self.login_qr_code
        item.setState_(1 if self.login_qr_code else 0)
        self.server.http_server.has_login_qr_code = self.login_qr_code

    def menu_item_log_display(self):
        item = self.app_objc.getMenuItemWithTitle_inMenu_("Log Display in Dashboard", "Options")
        self.log_display = not self.log_display
        item.setState_(1 if self.log_display else 0)
        self.server.http_server.log_display = self.log_display

    def menu_item_dev_tools(self):
        item = self.app_objc.getMenuItemWithTitle_inMenu_("Developer Tools", "Options")
        self.dev_tools = not self.dev_tools
        item.setState_(1 if self.dev_tools else 0)
        self.server.http_server.dev_tools = self.dev_tools

    def menu_item_language(self, language):
        item = self.app_objc.getMenuItemWithTitle_inMenu_("English", "Options")
        item.setState_(1 if language == "en" else 0)
        item = self.app_objc.getMenuItemWithTitle_inMenu_("French", "Options")
        item.setState_(1 if language == "fr" else 0)
        self.set_language(language)

    def menu_item_bridge(self, bridge):
        item = self.app_objc.getMenuItemWithTitle_inMenu_("Thymio Device Manager", "Options")
        item.setState_(1 if bridge == "tdm" else 0)
        item = self.app_objc.getMenuItemWithTitle_inMenu_("JSON WebSocket", "Options")
        item.setState_(1 if bridge == "jws" else 0)
        item = self.app_objc.getMenuItemWithTitle_inMenu_("No Robot", "Options")
        item.setState_(1 if bridge == "none" else 0)
        self.bridge = bridge
        self.server.set_bridge(bridge)
