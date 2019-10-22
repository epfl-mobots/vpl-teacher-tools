#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# server class without gui

from vpl3.baseapp import ApplicationBase
import time


class Application(ApplicationBase):

    def __init__(self, **kwargs):
        super(ApplicationBase, self).__init__(**kwargs)
        self.start_browser()
        print("VPL Server - " + self.address)

    def main_loop(self):
        while True:
            time.sleep(10)

    def writeln(self, str):
        print(str)
