#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# server gui with objc (for macOS only)

from vpl3.baseapp import ApplicationBase
from vpl3.cacaoapp import ApplicationObjCShell


class Application(ApplicationBase):

    def __init__(self, **kwargs):
        ApplicationBase.__init__(self, **kwargs)

        self.shorten_url = False

        self.app_objc = ApplicationObjCShell.alloc().init()
        self.app_objc.addMenu_withItems_("File", [
            [
                "Open Tools in Browser",
                "b",
                lambda sender: self.start_browser_tt()
            ]
        ])
        self.app_objc.addMenu_withItems_("Options", [
            [
                "Shorten URLs",
                None,
                lambda sender: self.menu_item_shorten_urls()
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
        ])
        self.app_objc.start()
        self.menu_item_shorten_urls()
        self.menu_item_language("fr")
        window = self.app_objc.createWindowWithTitle_width_height_x_y_(
            "VPL Server - " + self.address,
            300, 100,
            20, 20
        )
        self.status = self.app_objc.addLabelToWindow_title_width_x_y_(window,
                                                                      "",
                                                                      250, 10, 60)
        self.app_objc.addButtonToWindow_title_action_width_x_y_(window,
                                                                "Open tools in browser",
                                                                lambda sender: self.start_browser_tt(),
                                                                180, 60, 20)

    def main_loop(self):
        self.app_objc.run()

    def show_connection_status(self, str):
        if self.status:
            self.status.setStringValue_(str)

    def menu_item_shorten_urls(self):
        item = self.app_objc.getMenuItemWithTitle_inMenu_("Shorten URLs", "Options")
        self.shorten_url = not self.shorten_url
        item.setState_(1 if self.shorten_url else 0)
        self.server.http_server.full_url = not self.shorten_url

    def menu_item_language(self, language):
        item = self.app_objc.getMenuItemWithTitle_inMenu_("English", "Options")
        item.setState_(1 if language == "en" else 0)
        item = self.app_objc.getMenuItemWithTitle_inMenu_("French", "Options")
        item.setState_(1 if language == "fr" else 0)
        self.set_language(language)
