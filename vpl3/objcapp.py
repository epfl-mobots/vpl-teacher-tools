#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# server gui with objc (for macOS only)

from vpl3.baseapp import ApplicationBase

# macOS: sudo python3 -m pip install pyobjc
from Cocoa import *
from Foundation import NSObject
from objc import super

class ApplicationObjCShell(NSApplication):

    def init(self):
        self = super(NSApplication, self).init()
        if self is None:
            return self
        self.actionArray = []
        self.menuNames = []
        self.menuItems = []
        return self

    def setAction_forControl_(self, action, control):
        control.setTarget_(self)
        control.setAction_("forwardAction:")
        control.setTag_(len(self.actionArray))
        self.actionArray.append(action)

    def addMenu_withItems_(self, menuName, menuItems):
        self.menuNames.append(menuName)
        self.menuItems.append(menuItems)

    def start(self):
        NSApplication.sharedApplication()
        NSApp.setActivationPolicy_(NSApplicationActivationPolicyRegular)
        menubar = NSMenu.new().autorelease()

        def add_menu(name, items):
            menu_hook = NSMenuItem.new().autorelease()
            if name is not None:
                menu = NSMenu.alloc().initWithTitle_(name).autorelease()
            else:
                menu = NSMenu.new().autorelease()
            menu.setAutoenablesItems_(False)
            menubar.addItem_(menu_hook)
            sel = objc.selector(self.forwardAction_, signature=b"v@:@")
            for i in range(len(items)):
                menu_item = (NSMenuItem
                             .alloc()
                             .initWithTitle_action_keyEquivalent_(items[i][0],
                                                                  sel,
                                                                  items[i][1])
                             .autorelease())
                menu_item.setTarget_(self)
                menu_item.setTag_(len(self.actionArray))
                self.actionArray.append(items[i][2])
                menu_item.setEnabled_(True)
                menu.addItem_(menu_item)
            menu_hook.setSubmenu_(menu)

        add_menu(None, [
            (
                "Quit " + str(NSProcessInfo.processInfo().processName()),
                "q",
                NSApp.terminate_
            ),
        ])
        for i in range(len(self.menuNames)):
            add_menu(self.menuNames[i], self.menuItems[i])
        NSApp.setMainMenu_(menubar)

    def run(self):
        NSApp.activateIgnoringOtherApps_(True)
        NSApp.run()

    def createWindowWithTitle_width_height_x_y_(self, title, width, height, x, y):
        window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(NSMakeRect(0, 0, width, height), 1, 2, False).autorelease()
        window.cascadeTopLeftFromPoint_(NSMakePoint(x, y))
        window.setTitle_(title)
        window.makeKeyAndOrderFront_(0)
        return window

    def addLabelToWindow_title_width_x_y_(self, window, title, width, x, y):
        label = (NSTextField.alloc()
                  .initWithFrame_(NSMakeRect(x, y, width, 25))
                  .autorelease())
        label.setFont_(NSFont.systemFontOfSize_(14))
        label.setDrawsBackground_(False)
        label.setBordered_(False)
        label.setEditable_(False)
        label.setSelectable_(True)
        label.setStringValue_(title)
        window.contentView().addSubview_(label)
        return label

    def addButtonToWindow_title_action_width_x_y_(self, window, title, action, width, x, y):
        button = (NSButton.alloc()
                  .initWithFrame_(NSMakeRect(x, y, width, 25))
                  .autorelease())
        button.setBezelStyle_(NSRoundedBezelStyle)
        button.setTitle_(title)
        self.setAction_forControl_(action, button)
        window.contentView().addSubview_(button)
        return button

    @objc.IBAction
    def forwardAction_(self, sender):
        tag = sender.tag()
        self.actionArray[tag](sender)


class Application(ApplicationBase):

    def __init__(self, **kwargs):
        ApplicationBase.__init__(self, **kwargs)

        self.app_objc = ApplicationObjCShell.alloc().init()
        self.app_objc.addMenu_withItems_("File", [
            (
                "Open in Browser",
                "b",
                lambda sender: self.start_browser()
            )
        ])
        self.app_objc.start()
        window = self.app_objc.createWindowWithTitle_width_height_x_y_(
            "VPL Server - " + self.address,
            300, 200,
            20, 20
        )
        self.status = self.app_objc.addLabelToWindow_title_width_x_y_(window,
                                                                      "",
                                                                      250, 10, 160)
        self.app_objc.addButtonToWindow_title_action_width_x_y_(window,
                                                                "Open in Browser",
                                                                lambda sender: self.start_browser(),
                                                                180, 10, 130)

    def main_loop(self):
        self.app_objc.run()

    def show_connection_status(self, str):
        self.status.setStringValue_(str)
