#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# server gui with objc (for macOS only)

from vpl3tt.baseapp import ApplicationBase
from vpl3tt.cacaoapp import ApplicationObjCShell


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
        self.app_objc.addMenu_withItems_("View", [
            (
                "Log",
                "l",
                lambda sender: self.show_log(sender, True)
            )
        ])
        self.app_objc.start()
        window = self.app_objc.createWindowWithTitle_width_height_x_y_closable_(
            "VPL Server - " + self.address,
            300, 100,
            20, 20,
            False
        )
        self.status = self.app_objc.addLabelToWindow_title_width_x_y_(window,
                                                                      "",
                                                                      250, 10, 60)
        self.app_objc.addButtonToWindow_title_action_width_x_y_(window,
                                                                "Open tools in browser",
                                                                lambda sender: self.start_browser(),
                                                                180, 60, 20)

        self.log = None
        self.logText = None
        self.show_log(None, True)

    def main_loop(self):
        self.app_objc.run()

    def show_connection_status(self, str):
        self.status.setStringValue_(str)

    def writeln(self, str):
        self.app_objc.writeToTextOutput_text_(self.logText, str + "\n")

    def show_log(self, sender, visible):
        if visible:
            print(1)
            if self.log is None:
                print(2)
                self.log = self.app_objc.createWindowWithTitle_width_height_x_y_closable_(
                    "Console",
                    600, 400,
                    40, 200,
                    True
                )
                return
                print(3)
                self.logText = self.app_objc.addTextOutputToWindow_(self.log)
                print(4)
            else:
                self.log.makenKeyAndOrderFront_(sender)
        elif self.log is not None:
            self.log.orderOut_(sender)
