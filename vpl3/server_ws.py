#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# websocket server poc

# Websockets: see https://websockets.readthedocs.io/en/stable/intro.html

from vpl3.com_ws import WSServer
import json
import sys
import getopt
import websocket

from vpl3.db import Db


class VPLWebSocketServer:

    DEFAULT_PORT = 8001

    def __init__(self,
                 db_path=None,
                 ws_link_url=None,
                 ws_port=DEFAULT_PORT,
                 on_connect=None,
                 on_disconnect=None,
                 logger=None):
        self.db_path = db_path if db_path is not None else Db.DEFAULT_PATH
        self.ws = WSServer(ws_port, self)
        self.log_recipients = set()
        self.connection_count = 0
        self.on_connect_cb = on_connect
        self.on_disconnect_cb = on_disconnect
        self.logger = logger

        self.ws_link = None
        if ws_link_url:
            self.ws_link = websocket.create_connection(ws_link_url)

    def run(self):
        self.ws.run()

    def stop(self):
        self.ws.stop()

    def get_session_id(self, msg):
        if msg["sender"] and "sessionid" in msg["sender"]:
            return msg["sender"]["sessionid"]
        else:
            return None

    async def notify_dashboard(self):
        msg = {
            "sender": {
                "type": "server"
            },
            "type": "change",
            "data":
                list(
                    filter(
                        lambda i:
                            hasattr(i, "is_connected") and i.is_connected,
                        self.ws.get_instances()))
        }
        for ws in self.log_recipients:
            await self.ws.send(ws, msg)

    async def process_message(self, websocket, session_id, msg):
        if self.logger:
            log_str = (msg["sender"]["sessionid"]
                       if msg["sender"]["type"] == "vpl"
                       else msg["sender"]["type"])
            log_str += ": " + msg["type"]
            if msg["type"] == "log":
                log_str += " " + msg["data"]["type"]
                if msg["data"]["type"] == "cmd":
                    log_str += " " + msg["data"]["data"]["cmd"]
                    if "selected" in msg["data"]["data"]:
                        log_str += (" true"
                                    if msg["data"]["data"]["selected"]
                                    else " false")
                    if "state" in msg["data"]["data"]:
                        log_str += " " + msg["data"]["data"]["state"]
            self.logger(log_str)
        db = Db(self.db_path)
        if msg["type"] == "hello":
            websocket.is_connected = True
            if msg["sender"]["type"] == "dashboard":
                # register dashboard to receive all log messages
                self.log_recipients.add(websocket)
                await self.ws.send(websocket, {
                    "sender": {
                        "type": "server"
                    },
                    "type": "hello",
                    "data": self.ws.get_instances()
                })
            elif msg["sender"]["type"] == "vpl":
                # accept if a session id was provided
                tuple = db.get_session(msg["sender"]["sessionid"])
                if tuple is None:
                    await self.ws.send(websocket, {
                        "sender": {
                            "type": "server"
                        },
                        "type": "err",
                        "msg": "bad sessionid"
                    })
                else:
                    await self.ws.send(websocket, {
                        "sender": {
                            "type": "server"
                        },
                        "type": "hello",
                        "data": None
                    })
                    await self.notify_dashboard()
        elif msg["type"] == "bye":
            websocket.is_connected = False
            if msg["sender"]["type"] == "dashboard":
                # unregister dashboard
                self.log_recipients.remove(websocket)
            elif msg["sender"]["type"] == "vpl":
                tuple = db.get_session(msg["sender"]["sessionid"])
                if tuple is not None:
                    await self.notify_dashboard()
        elif msg["type"] in ("cmd", "file"):
            # forward command to all (or msg["rcpt"]) other websockets but self
            await self.ws.sendToAll(msg,
                                    except_websocket=websocket,
                                    only_websockets=msg["rcpt"])
        elif msg["type"] == "log":
            # save log message to database and forward to all dashboards
            db.add_log(msg["sender"]["sessionid"], "log",
                       json.dumps(msg["data"]))
            for ws in self.log_recipients:
                await self.ws.send(ws, msg)
            if self.ws_link:
                self.ws_link.send(json.dumps(msg))

    def on_connect(self, session_id):
        self.connection_count += 1
        if self.on_connect_cb:
            self.on_connect_cb(session_id)

    def on_disconnect(self, session_id):
        self.connection_count -= 1
        if self.on_disconnect_cb:
            self.on_disconnect_cb(session_id)


if __name__ == "__main__":
    ws_port = VPLWebSocketServer.DEFAULT_PORT
    ws_link_url = None
    try:
        arguments, values = getopt.getopt(sys.argv[1:],
                                          "", ["help", "port=", "link="])
    except getopt.error as err:
        print(str(err))
        sys.exit(1)
    for arg, val in arguments:
        if arg == "--help":
            print(f"""Usage: {sys.argv[0]} options
VPL 3 teacher tools websocket server

Options:
  --help     display help message and exit
  --link uri websocket uri for linked server (default: no linked server)
  --port num websocket server port number (default: {
                                           VPLWebSocketServer.DEFAULT_PORT})
            """)
            sys.exit(0)
        elif arg == "--port":
            ws_port = int(val)
        elif arg == "--link":
            ws_link_url = val

    wsserver = VPLWebSocketServer(ws_port=ws_port, ws_link_url=ws_link_url)
    wsserver.run()
