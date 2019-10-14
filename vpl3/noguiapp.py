#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# server class without gui

from vpl3.server import Server
from vpl3.urlutil import URLUtil
from vpl3.db import Db

import threading
import time


class Application:

    DEFAULT_HTTP_PORT = Server.DEFAULT_HTTP_PORT
    DEFAULT_WS_PORT = Server.DEFAULT_WS_PORT

    def __init__(self,
                 db_path=Db.DEFAULT_PATH,
                 http_port=DEFAULT_HTTP_PORT,
                 ws_port=DEFAULT_WS_PORT,
                 ws_link_url=None):
        self.http_port = http_port
        self.logger_lock = threading.Lock()
        self.server = Server(db_path=db_path,
                             http_port=http_port,
                             ws_port=ws_port,
                             ws_link_url=ws_link_url,
                             logger=self.logger)
        self.server.start()
        self.start_browser()

        print(f"VPL Server - {URLUtil.get_local_IP()}:{self.http_port}")

    def mainloop(self):
        while True:
            time.sleep(10)

    def logger(self, str):
        with self.logger_lock:
            print(str)

    def start_browser(self, event=None):
        URLUtil.start_browser(self.http_port, using="chrome")
