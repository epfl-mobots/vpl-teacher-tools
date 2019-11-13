#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# server gui partial base class (must be subclassed for specific gui pkg)

from vpl3.server import Server
from vpl3.urlutil import URLUtil
from vpl3.db import Db

import threading


class ApplicationBase:

    DEFAULT_HTTP_PORT = Server.DEFAULT_HTTP_PORT
    DEFAULT_WS_PORT = Server.DEFAULT_WS_PORT

    def __init__(self,
                 db_path=Db.DEFAULT_PATH,
                 http_port=None,
                 ws_port=DEFAULT_WS_PORT,
                 ws_link_url=None):
        self.logger_lock = threading.Lock()
        self.server = Server(db_path=db_path,
                             http_port=http_port,
                             ws_port=ws_port,
                             ws_link_url=ws_link_url,
                             logger=self.logger,
                             update_connection=self.update_connection,
                             initial_file_dir="data")
        self.server.add_files(if_new_db=True)
        self.server.start()
        self.http_port = self.server.get_http_port()
        self.address = f"{URLUtil.get_local_IP()}:{self.http_port}"

        # to implement in subclasses:
        # GUI initialization showing self.address w/ a way to call
        # self.start_browser_tt() and self.quit()

    def run(self):
        self.update_connection()
        self.main_loop()

    def logger(self, str):
        with self.logger_lock:
            self.writeln(str)

    def update_connection(self, session_id=None):
        str = f"""Number of connections: {
            self.server.ws_server.connection_count
            if self.server.ws_server
            else "-"
        }"""
        self.show_connection_status(str)

    def start_browser_tt(self, event=None):
        URLUtil.start_browser(port=self.http_port,
                              path="/tt.html",
                              using=["firefox", "chrome"])

    def quit(self):
        self.server.stop()
        self.exit_app()

    def main_loop(self):
        # must be overriden: must run event loop or sleep until quit
        pass

    def show_connection_status(self, str):
        # should be overriden: should display str as the connection status
        pass

    def writeln(self, str):
        # should be overriden: should add str+"\n" to log
        pass

    def exit_app(self):
        # should be overriden: should run event loop or sleep until quit
        pass
