
# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# Communication with TDM (just checking it's there)

import websocket


class TDMClient:

    def __init__(self, ws=None):
        self.ws = ws or "ws://127.0.0.1:8597"

    def check_connection(self):
        try:
            ws = websocket.create_connection(self.ws)
            ws.close()
        except ConnectionRefusedError:
            return False
        return True
