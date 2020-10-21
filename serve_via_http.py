#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# serve document via http

import http.server
import threading
import urllib
import mimetypes
import re
import sys
import os

from vpl3tt.cacaoapp import ApplicationObjCShell
from vpl3tt.urlutil import URLUtil



class Handler(http.server.BaseHTTPRequestHandler):

    DOC_ROOT = "doc"

    def do_get(self, head_only=False):
        """Implementation of GET and HEAD HTTP methods"""

        def send_reply(content):
            if "location" in content:
                self.send_response(http.server.HTTPStatus.MOVED_PERMANENTLY)
                self.send_header("Location", content["location"])
                self.end_headers()
            else:
                self.send_response(http.server.HTTPStatus.OK)
                self.send_header("Content-type", content["mime"])
                self.end_headers()
                if not head_only:
                    self.wfile.write(content["data"].encode())

        p = urllib.parse.urlparse(self.path)
        if p.path == "/":
            self.send_response(http.server.HTTPStatus.MOVED_PERMANENTLY)
            self.send_header("Location", self.server.default_path)
            self.end_headers()
            return
        elif (re.compile(r"^(/[-_a-zA-Z0-9]+(\.[a-zA-Z0-9]+)?)+")
              .match(p.path)):
            try:
                with open(self.server.doc_root + p.path, "rb") as f:
                    self.send_response(http.server.HTTPStatus.OK)
                    mimetype = mimetypes.MimeTypes().guess_type(p.path)
                    self.send_header("Content-type",
                                     mimetype[0]
                                     if mimetype[0]
                                     else "text/plain")
                    self.end_headers()
                    if not head_only:
                        self.wfile.write(f.read())
                return
            except OSError:
                pass

        self.send_response(http.server.HTTPStatus.NOT_FOUND)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        if not head_only:
            self.wfile.write(("404 Not Found\n" + p.path).encode())

    def do_GET(self):
        """Implementation of GET HTTP method"""
        self.do_get()

    def do_HEAD(self):
        """Implementation of HEAD HTTP method"""
        self.do_get(True)


class Server(http.server.HTTPServer):

    def __init__(self, path):
        super(http.server.HTTPServer, self) \
            .__init__(('', 0), Handler)
        path = os.path.abspath(path)
        r = re.compile(r"^(.*)(/[^/]*)$").match(path)
        self.doc_root = r[1]
        self.default_path = r[2]


class Application:

    DEFAULT_PORT = 8000

    def __init__(self, path):

        # http server
        self.httpd = Server(path)

        self.address = f"{URLUtil.get_local_IP()}:{self.httpd.server_port}"
        self.app_objc = ApplicationObjCShell.alloc().init()
        self.app_objc.addMenu_withItems_("File", [
            [
                "Open in Browser",
                "b",
                lambda sender: self.start_browser(),
            ],
        ])
        self.app_objc.start()
        window = self.app_objc.createWindowWithTitle_width_height_x_y_(
            "HTTP Server - " + self.address,
            300, 90,
            20, 20
        )
        self.app_objc.addButtonToWindow_title_action_width_x_y_(window,
                                                                "Open in browser",
                                                                lambda sender: self.start_browser(),
                                                                180, 60, 30)

    def run(self):

        def http_thread():
            self.httpd.serve_forever()

        self.http_thread = threading.Thread(target=http_thread)
        self.http_thread.start()

        self.app_objc.run()

    def start_browser(self):
        URLUtil.start_browser(self.httpd.server_port, using=["firefox", "chrome"])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"""Usage: {sys.argv[0]} filepath
File HTTP server
        """)
        sys.exit(0)

    app = Application(path=sys.argv[1])
    app.start_browser()
    app.run()
