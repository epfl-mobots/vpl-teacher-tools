#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# server app launcher with tkinter user interface

from vpl3.launch import launch
from vpl3.tkapp import Application
from vpl3.server_thymio import ThymioWebSocketServer

import threading
import asyncio

class ApplicationJWS(Application):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.server_thymio = None

        def thymio_thread():
            asyncio.set_event_loop(asyncio.new_event_loop())
            self.server_thymio = ThymioWebSocketServer()
            self.server_thymio.run()

        try:
            from vpl3.thymio import Connection
            Connection.serial_default_port()
            self.ws_thymio = threading.Thread(target=thymio_thread)
            self.ws_thymio.start()
        except Exception:
            self.disable_serial()


if __name__ == "__main__":
    launch(ApplicationJWS)
