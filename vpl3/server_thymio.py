#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# websocket-Thymios bridge with json packets

from vpl3.thymio import Connection
import asyncio
import websockets
import json
import sys
import getopt


class ThymioWebSocketServer:
    """
    Websocket server to bridge to Thymio(s) on serial port
    Received messages (JSON):
    {"type":"nodes"}
    {"type":"getvar","id":guid,"names":[name1,name2,...]}
    {"type":"setvar","id":guid,"var":{name1:array1,...}}
    {"type":"subscribe","id":guid,"names":[name1,name2,...]}
    {"type":"run","id":guid,"bc":[bytecode]}
    Sent messages (JSON):
    {"type":"connect","id":guid,"name":name,"human":user-specified name,"descr":...}
    {"type":"disconnect","id":guid}
    {"type":"var","id":guid,"var":{name1:array1,...}}
    """

    DEFAULT_PORT = 8002

    def __init__(self,
                 ws_port=DEFAULT_PORT,
                 on_connect=None,
                 on_disconnect=None):

        async def ws_handler(websocket, path):
            self.websockets.add(websocket)
            websocket.subscriptions = {}
            try:
                async for message in websocket:
                    msg = json.loads(message)
                    await self.process_message(websocket, msg)
            finally:
                self.websockets.remove(websocket)

        print("ThymioWebSocketServer __init__", "port", ws_port)
        self.loop = asyncio.get_event_loop()
        self.ws_server = websockets.serve(ws_handler, port=ws_port)
        self.websockets = set()
        self.nodes = {}
        self.thymio = None
        self.connection_count = 0

        self.on_connect_cb = on_connect
        self.on_disconnect_cb = on_disconnect

    async def send(self, websocket, msg):
        try:
            await websocket.send(msg
                                 if isinstance(msg, str)
                                 else json.dumps(msg))
        except websockets.ConnectionClosed:
            if websocket in self.websockets:
                self.websockets.remove(websocket)

    async def send_to_all(self, msg):
        for websocket in self.websockets:
            await self.send(websocket, msg)

    def run(self):

        async def on_connection_changed(node_id, connected):
            print("Connection" if connected else "Disconnection", node_id)
            remote_node = self.thymio.remote_nodes[node_id]
            msg = {
                "type": "connect" if connected else "disconnect",
                "id": remote_node.device_uuid
            }
            if connected:
                # add node description, useful for compiler
                msg["descr"] = {
                    "name": remote_node.name,
                    "maxVarSize": remote_node.max_var_size,
                    "variables": [
                        {
                            "name": name,
                            "size": remote_node.var_size[name]
                        } for name in remote_node.named_variables
                    ],
                    "localEvents": [
                        {
                            "name": name
                        } for name in remote_node.local_events
                    ],
                    "nativeFunctions": [
                        {
                            "name": name,
                            "args": remote_node.native_functions_arg_sizes[name]
                        } for name in remote_node.native_functions
                    ]
                }
                # retain node
                self.nodes[node_id] = msg
            else:
                # discard node
                del self.nodes[node_id]
            await self.send_to_all(msg)

        async def on_variables_received(node_id):
            for websocket in self.websockets:
                if node_id in websocket.subscriptions:
                    msg = {
                        "type": "var",
                        "id": self.thymio.remote_nodes[node_id].device_uuid,
                        "var": {
                            name: self.thymio[node_id][name]
                            for name in websocket.subscriptions[node_id]
                        }
                    }
                    await self.send(websocket, msg)

        self.thymio = Connection.serial(discover_rate=2, refreshing_rate=1,
                                        loop=asyncio.get_event_loop())
        self.thymio.on_connection_changed = on_connection_changed
        self.thymio.on_variables_received = on_variables_received

        self.loop.run_until_complete(self.ws_server)
        self.loop.run_forever()

    def stop(self):
        self.ws_server.stop()
        self.thymio.shutdown()

    async def process_message(self, websocket, msg):
        try:
            type = msg["type"]
            if type == "nodes":
                for node in self.nodes.values():
                    await self.send(websocket, node)
            else:
                guid = msg["id"]
                node_id = self.thymio.uuid_to_node_id(guid)
                if node_id is not None:
                    if type == "getvar":
                        reply = {
                            "type": "var",
                            "id": guid,
                            "var": {
                                name: self.thymio[node_id][name]
                                for name in msg["names"]
                            }
                        }
                        await self.send(websocket, reply)
                    elif type == "subscribe":
                        websocket.subscriptions[node_id] = msg["names"]
                    elif type == "setvar":
                        v = msg["var"]
                        for name in v:
                            self.thymio[node_id][name] = v[name]
                    elif type == "run":
                        bc = msg["bc"]
                        self.thymio.set_bytecode(node_id, bc)
                        self.thymio.run(node_id)
                    else:
                        reply = {
                            "type": "err",
                            "msg": "unknown type"
                        }
                        await self.send(websocket, reply)
        except Exception:
            pass

    def on_connect(self):
        self.connection_count += 1
        if self.on_connect_cb:
            self.on_connect_cb(session_id)

    def on_disconnect(self):
        self.connection_count -= 1
        if self.on_disconnect_cb:
            self.on_disconnect_cb(session_id)


if __name__ == "__main__":
    ws_port = ThymioWebSocketServer.DEFAULT_PORT
    try:
        arguments, values = getopt.getopt(sys.argv[1:],
                                          "", ["help", "port=", "link="])
    except getopt.error as err:
        print(str(err))
        sys.exit(1)
    for arg, val in arguments:
        if arg == "--help":
            print(f"""Usage: {sys.argv[0]} options
VPL 3 Thymio websocket server

Options:
  --help     display help message and exit
  --port num websocket server port number (default: {
                                           ThymioWebSocketServer.DEFAULT_PORT})
            """)
            sys.exit(0)
        elif arg == "--port":
            ws_port = int(val)

    wsserver = ThymioWebSocketServer(ws_port=ws_port)
    wsserver.run()
