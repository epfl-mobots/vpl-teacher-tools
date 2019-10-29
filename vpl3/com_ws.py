# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# Websockets: see https://websockets.readthedocs.io/en/stable/intro.html

import asyncio
import websockets
import json


class WSServer:

    DEFAULT_PORT = 8001

    def __init__(self, port, context):
        self.instances = set()

        async def ws_handler(websocket, path):
            websocket.session_id = None
            no_message_yet = True
            self.instances.add(websocket)
            try:
                async for message in websocket:
                    print(message)
                    message_dec = json.loads(message)
                    if websocket.session_id is None:
                        id = context.get_session_id(message_dec)
                        if id:
                            websocket.session_id = id
                    if no_message_yet:
                        context.on_connect(websocket.session_id)
                        no_message_yet = False
                    await context.process_message(websocket,
                                                  websocket.session_id,
                                                  message_dec)
            finally:
                self.instances.remove(websocket)
                if not no_message_yet:
                    context.on_disconnect(websocket.session_id)

        self.context = context
        if port is None:
            try:
                self.ws_server = websockets.serve(ws_handler, port=self.DEFAULT_PORT)
            except:
                self.ws_server = websockets.serve(ws_handler, port=0)
        else:
            self.ws_server = websockets.serve(ws_handler, port=port)
        self.loop = asyncio.get_event_loop()

    def run(self):
        self.loop.run_until_complete(self.ws_server)
        self.loop.run_forever()

    def stop(self):
        """Stop websocket server in a thread-safe way"""
        def s():
            for websocket in self.instances:
                websocket.close()
                # bug: should await I don't know how
                # will produce errors on exit which look harmless
            self.loop.stop()
        self.loop.call_soon_threadsafe(s)

    def get_instances(self):
        return list(map(lambda ws: ws.session_id, self.instances))

    async def send(self, websocket, msg):
        try:
            await websocket.send(msg
                                 if isinstance(msg, str)
                                 else json.dumps(msg))
        except websockets.ConnectionClosed:
            if websocket in self.instances:
                self.instances.remove(websocket)

    async def sendToAll(self, msg,
                        except_websocket=None,
                        only_websockets=None):
        for ws in self.instances:
            if (only_websockets is None
                or ws.session_id not in only_websockets) \
               and ws is not except_websocket:
                await self.send(ws, msg)
