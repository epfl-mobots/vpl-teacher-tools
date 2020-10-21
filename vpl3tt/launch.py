# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# server app launcher
# usage:
# from vpl3tt.launch import launch
# from vpl3tt.tkapp import Application
# if __name__ == "__main__": launch(Application)
# (or replace tkapp with wxapp or objcapp)

from vpl3tt.db import Db
from vpl3tt.server import Server

import getopt
import sys
import logging


def launch(App):
    http_port = None
    ws_port = App.DEFAULT_WS_PORT
    timeout = Server.DEFAULT_START_TIMEOUT
    ws_link_url = None
    db_path = Db.DEFAULT_PATH
    language = "fr"
    try:
        arguments, values = getopt.getopt(sys.argv[1:],
                                          "",
                                          [
                                              "db=",
                                              "help",
                                              "http-port=",
                                              "language=",
                                              "link=",
                                              "log=",
                                              "timeout=",
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
  --http-port num HTTP port, or auto (default: auto, trying first {App.DEFAULT_HTTP_PORT})
  --language code language code such as "fr" (default: {language})
  --log level     set log level
                  (debug, info, warning (default), error, critical)
  --link uri      websocket uri for linked server (default: no linked server)
  --timeout t     timeout in seconds to launch servers (default: {Server.DEFAULT_START_TIMEOUT})
  --ws-port num   websocket server port, or auto
                  (default: auto, trying first {App.DEFAULT_WS_PORT})
            """)
            sys.exit(0)
        elif arg == "--http-port":
            http_port = int(val)
        elif arg == "--ws-port":
            ws_port = int(val)
        elif arg == "--timeout":
            timeout = float(val)
        elif arg == "--link":
            ws_link_url = val
        elif arg == "--log":
            log_level = getattr(logging, val.upper(), None)
            if not isinstance(log_level, int):
                raise ValueError(f"Invalid log level: {val}")
            logging.basicConfig(level=log_level)

    logging.info(f"sys.version: {sys.version}")
    logging.info(f"sys.platform: {sys.platform}")

    app = App(db_path=db_path,
              http_port=http_port,
              ws_port=ws_port,
              timeout=timeout,
              ws_link_url=ws_link_url,
              language=language if language != "en" else None)
    app.run()
