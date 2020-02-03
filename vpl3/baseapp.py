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
                 ws_link_url=None,
                 language=None,
                 full_url=False):
        self.logger_lock = threading.Lock()
        self.server = Server(db_path=db_path,
                             http_port=http_port,
                             ws_port=ws_port,
                             ws_link_url=ws_link_url,
                             language=language,
                             full_url=full_url,
                             logger=self.logger,
                             update_connection=self.update_connection,
                             update_robots=self.update_robots,
                             initial_file_dir="data")
        self.server.add_files(if_new_db=True)
        self.server.start()
        self.http_port = self.server.get_http_port()
        self.no_serial = False
        self.language = language
        self.bridge = "none"  # "tdm" or "jws" or "none"
        self.full_url = full_url

        # to implement in subclasses:
        # GUI initialization showing self.tt_url() w/ a way to call
        # self.start_browser_tt() and self.quit()

    def tt_abs_path(self):
        return f"/tt{'.' + self.language if self.language and self.language != 'en' else ''}.html"

    def tt_url(self, short=False):
        return f"{'' if short else 'http://'}{URLUtil.get_local_IP()}:{self.http_port}{self.tt_abs_path()}"

    def set_bridge(self, bridge):
        self.bridge = bridge
        self.server.set_bridge(bridge)

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

    def update_robots(self, session_id=None):
        if self.bridge == "jws":
            str = f"""Number of robots: {
                self.server.thymio_server.robot_count
                if self.server.thymio_server
                else "-"
            }"""
            self.show_robots_status(str)
        else:
            self.show_robots_status("")

    def start_browser_tt(self):
        path = self.tt_abs_path()
        URLUtil.start_browser(port=self.http_port,
                              path=path,
                              using=["firefox", "chrome"])

    def set_language(self, language):
        self.language = language
        self.server.language = language
        self.server.http_server.language = language

    def quit(self):
        self.server.stop()
        self.exit_app()

    def main_loop(self):
        # must be overriden: must run event loop or sleep until quit
        pass

    def show_connection_status(self, str):
        # should be overriden: should display str as the connection status
        pass

    def show_robots_status(self, str):
        # should be overriden: should display str as the robots status
        pass

    def writeln(self, str):
        # should be overriden: should add str+"\n" to log
        pass

    def exit_app(self):
        # should be overriden: should run event loop or sleep until quit
        pass
