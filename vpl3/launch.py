# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# server app launcher
# usage:
# from vpl3.launch import launch
# from vpl3.tkapp import Application
# if __name__ == "__main__": launch(Application)
# (or replace tkapp with wxapp or objcapp)

from vpl3.db import Db

import getopt
import sys


def launch(App):
    http_port = None
    ws_port = App.DEFAULT_WS_PORT
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
                                              "link=",
                                              "ws-port=",
                                              "language="
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
  --link uri      websocket uri for linked server (default: no linked server)
  --ws-port num   websocket server port, or auto (default: auto, trying first {App.DEFAULT_WS_PORT})
            """)
            sys.exit(0)
        elif arg == "--http-port":
            http_port = int(val)
        elif arg == "--ws-port":
            ws_port = int(val)
        elif arg == "--link":
            ws_link_url = val

    app = App(db_path=db_path,
              http_port=http_port,
              ws_port=ws_port,
              ws_link_url=ws_link_url,
              language=language if language is not "en" else None)
    app.run()
