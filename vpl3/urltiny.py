# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# URL shortcuts

import os
import hashlib


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

    def digest_to_key(self, digest):
        key = ""
        for i in range(self.length):
            key += chr(97 + digest[i] % 26)
        return key

    def add(self, url):
        digest =  hashlib.sha256(bytes(url,"utf-8")).digest()
        key = self.digest_to_key(digest)
        self.dict[key] = url
        return key

    def get(self, key):
        return self.dict[key]
