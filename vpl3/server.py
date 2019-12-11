#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# server supervisor

from vpl3.server_http import VPLHTTPServer
from vpl3.server_ws import VPLWebSocketServer
from vpl3.server_thymio import ThymioWebSocketServer
from vpl3.db import Db

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
                 language=None,
                 full_url=False,
                 logger=None,
                 update_connection=None,
                 update_robots=None,
                 initial_file_dir=None):
        self.db_path = db_path
        self.initial_file_dir = initial_file_dir
        self.http_port = http_port
        self.http = None
        self.http_server = None
        self.ws_port = ws_port
        self.ws_link_url = ws_link_url
        self.bridge = "none"
        self.language = language
        self.full_url = full_url
        self.ws = None
        self.ws_server = None
        self.ws_thymio = None
        self.thymio_server = None
        self.logger = logger
        self.update_con = update_connection
        self.update_robots = update_robots

    def add_files(self, if_new_db=False):
        db = Db(self.db_path)
        if db.new_db:
            import os
            import re
            f = re.compile("^[^.]")
            filenames = [
                os.path.join(self.initial_file_dir, filename)
                for filename in os.listdir(self.initial_file_dir)
                if f.match(filename) and
                   os.path.isfile(os.path.join(self.initial_file_dir, filename))
            ]
            if len(filenames) > 0:
                db.add_local_files(filenames)

    def set_bridge(self, bridge):
        if self.bridge != bridge:
            if self.bridge == "jws" and self.thymio_server:
                self.thymio_server.stop()
                self.ws_thymio.wait()
                self.thymio_server = None
            self.bridge = bridge
            self.http_server.bridge = bridge
            if self.bridge == "jws":
                def thymio_thread():
                    asyncio.set_event_loop(asyncio.new_event_loop())
                    self.thymio_server = ThymioWebSocketServer(
                        on_connect=self.update_robots,
                        on_disconnect=self.update_robots)
                    self.thymio_server.run()
                try:
                    from vpl3.thymio import Connection
                    Connection.serial_default_port()
                    self.ws_thymio = threading.Thread(target=thymio_thread)
                    self.ws_thymio.start()
                except Exception:
                    self.disable_serial()

    def start(self):

        # let know the main thread that both servers have been started
        http_started = False
        ws_started = False
        servers_started = threading.Event()

        def http_thread():
            self.http_server = VPLHTTPServer(db_path=self.db_path,
                                             http_port=self.http_port,
                                             language=self.language,
                                             full_url=self.full_url,
                                             logger=self.logger)
            self.http_port = self.http_server.get_port()
            nonlocal http_started
            http_started = True
            if ws_started:
                servers_started.set()
            self.http_server.run()

        def ws_thread():
            asyncio.set_event_loop(asyncio.new_event_loop())
            self.ws_server = VPLWebSocketServer(db_path=self.db_path,
                                                logger=self.logger,
                                                ws_port=self.ws_port,
                                                ws_link_url=self.ws_link_url,
                                                on_connect=self.update_con,
                                                on_disconnect=self.update_con)
            nonlocal ws_started
            ws_started = True
            if http_started:
                servers_started.set()
            self.ws_server.run()

        self.http = threading.Thread(target=http_thread)
        self.ws = threading.Thread(target=ws_thread)
        self.http.start()
        self.ws.start()

        # wait until both servers have been started before returning,
        # so that self.http_port and self.ws_port are known
        servers_started.wait(timeout=2)

    def stop(self):
        self.http_server.stop()
        self.ws_server.stop()
        self.http.join()
        self.ws.join()

    def get_http_port(self):
        return self.http_port
