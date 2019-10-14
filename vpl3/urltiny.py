#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# URL shortcuts

import os

class URLShortcuts:

    def __init__(self, length=5):
        self.length = length
        self.dict = {}
        self.num = 26 ** length
        b = os.urandom(2)
        self.step = 11 ** length + (b[0] << 1 | b[1] << 10)
        if self.step % 13 == 0:
            # no common factor with self.num
            self.step += 2
        self.state = 0
        b = os.urandom(4)
        self.state = (b[0] | b[1] << 9 | b[2] << 18 | b[3] << 27) % self.num

    def current_key(self):
        key = ""
        for i in range(self.length):
            key += chr(97 + self.state // 26 ** i % 26)
        return key

    def next_key(self):
        self.state = (self.state + self.step) % self.num
        return self.current_key()

    def add(self, url):
        key = self.next_key()
        self.dict[key] = url
        return key

    def get(self, key):
        return self.dict[key]
