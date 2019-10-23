#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# server gui with objc (for macOS only)

from vpl3.baseapp import ApplicationBase
from vpl3.cacaoapp import ApplicationObjCShell


class Application(ApplicationBase):

    def __init__(self, **kwargs):
        ApplicationBase.__init__(self, **kwargs)

        self.app_objc = ApplicationObjCShell.alloc().init()
        self.app_objc.addMenu_withItems_("File", [
            (
                "Open Tools in Browser",
                "b",
                lambda sender: self.start_browser()
            )
        ])
        self.app_objc.start()
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
                                                                lambda sender: self.start_browser(),
                                                                180, 60, 20)

    def main_loop(self):
        self.app_objc.run()

    def show_connection_status(self, str):
        self.status.setStringValue_(str)
