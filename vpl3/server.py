#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# server supervisor

from vpl3.server_http import VPLHTTPServer
from vpl3.server_ws import VPLWebSocketServer

import threading
import asyncio


class Server:

    DEFAULT_HTTP_PORT = VPLHTTPServer.DEFAULT_PORT
    DEFAULT_WS_PORT = VPLWebSocketServer.DEFAULT_PORT

    def __init__(self,
                 db_path=None,
                 http_port=DEFAULT_HTTP_PORT,
                 ws_port=DEFAULT_WS_PORT,
                 ws_link_url=None,
                 logger=None,
                 update_connection=None):
        self.db_path = db_path
        self.http_port = http_port
        self.http = None
        self.http_server = None
        self.ws_port = ws_port
        self.ws_link_url = ws_link_url
        self.ws = None
        self.ws_server = None
        self.logger = logger
        self.update_con = update_connection

    def start(self):

        def http_thread():
            self.http_server = VPLHTTPServer(db_path=self.db_path,
                                             http_port=self.http_port,
                                             logger=self.logger)
            self.http_server.run()

        def ws_thread():
            asyncio.set_event_loop(asyncio.new_event_loop())
            self.ws_server = VPLWebSocketServer(db_path=self.db_path,
                                                logger=self.logger,
                                                ws_port=self.ws_port,
                                                ws_link_url=self.ws_link_url,
                                                on_connect=self.update_con,
                                                on_disconnect=self.update_con)
            self.ws_server.run()

        self.http = threading.Thread(target=http_thread)
        self.ws = threading.Thread(target=ws_thread)
        self.http.start()
        self.ws.start()

    def stop(self):
        self.http_server.stop()
        self.ws_server.stop()
        self.http.join()
        self.ws.join()
