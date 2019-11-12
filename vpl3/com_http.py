#!/usr/bin/python3

# server poc

# Websockets: see https://websockets.readthedocs.io/en/stable/intro.html

import http.server
import urllib
import mimetypes
import re

dict_get = {}
list_get_any = []
dict_post = {}


class DocFilterSet:
    """Filter text documents before serving them"""

    def __init__(self):
        self.filters = []

    class Filter:

        def __init__(self, fun, path_regex=None):
            self.fun = fun
            self.re = re.compile(path_regex) if path_regex is not None else None

        def process(self, path, content):
            if self.re is None or self.re.search(path):
                return self.fun(content)
            else:
                return content


    def add_filter(self, fun, path_regex=None):
        self.filters.append(self.Filter(fun, path_regex))

    def process(self, path, content):
        for f in self.filters:
            content = f.process(path, content)
        return content


class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """Request handler class for HTTP server"""

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
        if p.path in dict_get:
            content = dict_get[p.path](self.server.context, self)
            send_reply(content)
        else:
            if (re.compile(r"^(/[-_a-zA-Z0-9]+(\.[a-zA-Z0-9]+)?)+")
                  .match(p.path)):
                try:
                    with open(HTTPRequestHandler.DOC_ROOT + p.path, "rb") as f:
                        self.send_response(http.server.HTTPStatus.OK)
                        mimetype = mimetypes.MimeTypes().guess_type(p.path)
                        self.send_header("Content-type",
                                         mimetype[0]
                                         if mimetype[0]
                                         else "text/plain; charset=utf-8")
                        self.end_headers()
                        if not head_only:
                            content = f.read()
                            content = self.server.doc_filter_set.process(p.path,
                                                                         content)
                            self.wfile.write(content)
                    return
                except OSError:
                    pass

            for f in list_get_any:
                content = f(p.path, self.server.context, self)
                if content is not None:
                    send_reply(content)
                    return

            self.send_response(http.server.HTTPStatus.NOT_FOUND)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            if not head_only:
                self.wfile.write(("404 Not Found\n" + p.path).encode())

    def do_GET(self):
        """Implementation of GET HTTP method"""
        self.do_get()

    def do_HEAD(self):
        """Implementation of HEAD HTTP method"""
        self.do_get(True)

    def do_POST(self):
        """Implementation of POST HTTP method"""
        p = urllib.parse.urlparse(self.path)
        if p.path in dict_post:
            content = dict_post[p.path](self.server.context, self)
            if "location" in content:
                self.send_response(http.server.HTTPStatus.MOVED_PERMANENTLY)
                self.send_header("Location", content["location"])
            else:
                self.send_response(http.server.HTTPStatus.OK)
                self.send_header("Content-type", content["mime"])
            self.end_headers()
            self.wfile.write(content["data"].encode())
        else:
            self.send_response(http.server.HTTPStatus.NOT_FOUND)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(("404 Not Found\n" + p.path).encode())

    def log_message(self, format, *args):
        if self.server.logger is not None:
            self.server.logger(format % args)


def http_get(path):
    def register(fun):
        dict_get[path] = fun
        return fun
    return register

def http_get_any(fun):
    list_get_any.append(fun)
    return fun

def http_post(path):
    def register(fun):
        dict_post[path] = fun
        return fun
    return register


class HTTPServerWithContext(http.server.HTTPServer):

    DEFAULT_PORT = 8000

    def __init__(self, context=None, port=None, logger=None):
        if port is None:
            try:
                super(http.server.HTTPServer, self) \
                    .__init__(('', self.DEFAULT_PORT), context.handler)
            except:
                super(http.server.HTTPServer, self) \
                    .__init__(('', 0), context.handler)
        else:
            super(http.server.HTTPServer, self) \
                .__init__(('', port), context.handler)
        self.context = context
        self.doc_filter_set = DocFilterSet()
        self.logger = logger

    def get_port(self):
        return self.server_port

    def add_filter(self, fun, path_regex=None):
        self.doc_filter_set.add_filter(fun, path_regex)
