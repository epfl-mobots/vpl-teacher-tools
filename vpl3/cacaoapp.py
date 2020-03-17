#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# pyobjc-based application class (for macOS only)

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
        self.menus = []
        self.menuItems = []
        self.aboutAppAction = None
        return self

    def setAction_forControl_(self, action, control):
        control.setTarget_(self)
        control.setAction_("forwardAction:")
        control.setTag_(len(self.actionArray))
        self.actionArray.append(action)

    def addMenu_withItems_(self, menuName, menuItems):
        self.menuNames.append(menuName)
        self.menuItems.append(menuItems)

    def getMenuWithTitle_(self, menuTitle):
        for i in range(len(self.menuNames)):
            if self.menuNames[i] == menuTitle:
                return self.menus[i]

    def getMenuItemWithTitle_inMenu_(self, menuItemTitle, menuTitle):
        for i in range(len(self.menuNames)):
            if self.menuNames[i] == menuTitle:
                for j in range(len(self.menuItems[i])):
                    if (self.menuItems[i][j] and
                        self.menuItems[i][j][0] == menuItemTitle):
                        return self.menuItems[i][j][3]

    def start(self):
        NSApplication.sharedApplication()
        NSApp.setActivationPolicy_(NSApplicationActivationPolicyRegular)
        menubar = NSMenu.new().autorelease()

        def add_menu(name, items):
            menu_hook = NSMenuItem.new().autorelease()
            if name is not None:
                menu = NSMenu.alloc().initWithTitle_(name).autorelease()
                self.menus.append(menu)
            else:
                menu = NSMenu.new().autorelease()
            menu.setAutoenablesItems_(False)
            menubar.addItem_(menu_hook)
            sel = objc.selector(self.forwardAction_, signature=b"v@:@")
            for i in range(len(items)):
                if items[i]:
                    shortcut = items[i][1] or ""
                    menu_item = (NSMenuItem
                                 .alloc()
                                 .initWithTitle_action_keyEquivalent_(items[i][0],
                                                                      sel,
                                                                      shortcut)
                                 .autorelease())
                    menu_item.setTarget_(self)
                    menu_item.setTag_(len(self.actionArray))
                    self.actionArray.append(items[i][2])
                    menu_item.setEnabled_(True)
                    menu.addItem_(menu_item)
                    if len(items[i]) >= 4:
                        items[i][3] = menu_item
                    else:
                        items[i].append(menu_item)
                else:
                    menu.addItem_(NSMenuItem.separatorItem())
            menu_hook.setSubmenu_(menu)

        quit_menu_entry = [
            "Quit " + str(NSProcessInfo.processInfo().processName()),
            "q",
            NSApp.terminate_
        ]
        add_menu(None, [
                [
                    "About " + str(NSProcessInfo.processInfo().processName()),
                    None,
                    self.aboutAppAction
                ],
                None,
                quit_menu_entry
            ] if self.aboutAppAction else [
                quit_menu_entry,
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

    def addDrawingToWindow_draw_x_y_width_height_(self, window, draw, x, y, w, h):

        class Drawing(NSView):
            def initWithFrame_draw_(self, frame, draw):
                self = NSView.initWithFrame_(self, frame)
                if self is not None:
                    self.draw = draw
                return self
            def initWithFrame_(self, frame):
                self = super(NSView, self).initWithFrame_(frame)
                if self is not None:
                    self.draw = None
                return self
            def drawRect_(self, rect):
                if self.draw is None:
                    NSColor.yellowColor().set()
                    NSRectFill(rect)
                else:
                    self.draw(rect)

        drawing = (Drawing.alloc()
                   .initWithFrame_draw_(NSMakeRect(x, y, w, h), draw)
                   .autorelease())
        window.contentView().addSubview_(drawing)
        return drawing

    @objc.IBAction
    def forwardAction_(self, sender):
        tag = sender.tag()
        self.actionArray[tag](sender)
