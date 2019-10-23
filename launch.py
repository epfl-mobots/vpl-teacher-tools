#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# server app launcher

from vpl3.tkapp import Application
# from vpl3.wxapp import Application
# from vpl3.objcapp import Application
# from vpl3.noguiapp import Application
from vpl3.db import Db

import getopt
import sys


if __name__ == "__main__":
    http_port = Application.DEFAULT_HTTP_PORT
    ws_port = Application.DEFAULT_WS_PORT
    ws_link_url = None
    db_path = Db.DEFAULT_PATH
    try:
        arguments, values = getopt.getopt(sys.argv[1:],
                                          "",
                                          [
                                              "db=",
                                              "help",
                                              "http-port=",
                                              "link=",
                                              "ws-port=",
                                          ])
    except getopt.error as err:
        print(str(err))
        sys.exit(1)
    for arg, val in arguments:
        if arg == "--help":
            print(f"""Usage: {sys.argv[0]} options
VPL 3 teacher tools server

Options:
  --db path       path of sqlite database (default: {Db.DEFAULT_PATH})
  --help          display help message and exit
  --http-port num HTTP port (default: {Application.DEFAULT_HTTP_PORT})
  --link uri      websocket uri for linked server (default: no linked server)
  --ws-port num   websocket server port number (default: {Application.DEFAULT_WS_PORT})
            """)
            sys.exit(0)
        elif arg == "--http-port":
            http_port = int(val)
        elif arg == "--ws-port":
            ws_port = int(val)
        elif arg == "--link":
            ws_link_url = val

    app = Application(db_path=db_path,
                      http_port=http_port,
                      ws_port=ws_port,
                      ws_link_url=ws_link_url)
    app.run()
