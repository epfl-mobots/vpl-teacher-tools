#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# server poc

# Websockets: see https://websockets.readthedocs.io/en/stable/intro.html

import urllib
from vpl3.com_http \
    import (
        HTTPServerWithContext, HTTPRequestHandler,
        http_get, http_get_any, http_post
    )
import json

from vpl3.db import Db
from vpl3.urlutil import URLUtil
from vpl3.urltiny import URLShortcuts
import sys
import getopt


class VPLHTTPRequestHandler(HTTPRequestHandler):

    def __init__(self, request, client_address, server):
        HTTPRequestHandler.__init__(self, request, client_address, server)


class VPLHTTPServer:

    DEFAULT_PORT = 8000

    def __init__(self,
                 db_path=Db.DEFAULT_PATH,
                 http_port=DEFAULT_PORT,
                 logger=None):
        self.http_port = http_port
        self.db_path = db_path
        self.handler = VPLHTTPRequestHandler
        self.url_shortcuts = URLShortcuts()
        self.httpd = HTTPServerWithContext(context=self,
                                           port=http_port, logger=logger)
        self.groups = []

    def run(self):
        self.httpd.serve_forever()

    def stop(self):
        self.httpd.shutdown()

    def query_param(handler):
        p = urllib.parse.urlparse(handler.path)
        q = urllib.parse.parse_qs(p.query, keep_blank_values=True)
        return q

    def get_data(handler, text=True):
        content_length = int(handler.headers['Content-Length'])
        post_data = handler.rfile.read(content_length)
        return post_data.decode("utf-8") if text else post_data

    def error(msg):
        return {
            "mime": "application/json",
            "data": json.dumps({
                "status": "err",
                "msg": msg
            }, indent=4)
        }

    def call_api(self, fun, *args, **kwargs):
        try:
            result = fun(Db(self.db_path), *args, **kwargs)
            return {
                "mime": "application/json",
                "data": json.dumps({
                    "status": "ok",
                    "result": result
                }, indent=4)
            }
        except ValueError as ve:
            return VPLHTTPServer.error(ve.args[0])

    @http_get("/")
    def http_get_root(self, handler):
        return {
            "location": "/index.html"
        }

    @http_get("/api/groups")
    def http_get_groups(self, handler):
        return {
            "mime": "application/json",
            "data": json.dumps(self.groups, indent=4)
        }

    @http_get("/api/pairing")
    def http_get_pairing(self, handler):
        return {
            "mime": "application/json",
            "data": json.dumps(None)
        }

    @http_get("/api/deleteAllStudents")
    def http_get_api_deleteAllStudents(self, handler):
        return self.call_api(Db.delete_all_students)

    @http_get("/api/addStudent")
    def http_get_api_addStudent(self, handler):
        q = VPLHTTPServer.query_param(handler)
        if "name" not in q:
            return VPLHTTPServer.error("Missing name")
        return self.call_api(Db.add_student, q["name"][0])

    @http_get("/api/removeStudent")
    def http_get_api_removeStudent(self, handler):
        q = VPLHTTPServer.query_param(handler)
        if "name" not in q:
            return VPLHTTPServer.error("Missing name")
        return self.call_api(Db.remove_student, q["name"][0])

    @http_get("/api/listStudents")
    def http_get_api_listStudents(self, handler):
        return self.call_api(Db.list_students)

    @http_get("/api/addGroup")
    def http_get_api_addGroup(self, handler):
        q = VPLHTTPServer.query_param(handler)
        if "group" not in q:
            return VPLHTTPServer.error("Missing group")
        return self.call_api(Db.add_group, q["group"][0])

    @http_get("/api/removeGroup")
    def http_get_api_removeGroup(self, handler):
        q = VPLHTTPServer.query_param(handler)
        if "group" not in q:
            return VPLHTTPServer.error("Missing group")
        return self.call_api(Db.remove_group, q["group"][0])

    @http_get("/api/listGroups")
    def http_get_api_listGroups(self, handler):
        return self.call_api(Db.list_groups)

    @http_get("/api/addStudentToGroup")
    def http_get_api_addStudentToGroup(self, handler):
        q = VPLHTTPServer.query_param(handler)
        if "name" not in q:
            return VPLHTTPServer.error("Missing name")
        if "group" not in q:
            return VPLHTTPServer.error("Missing group")
        return self.call_api(Db.add_student_to_group,
                             q["name"][0], q["group"][0])

    @http_get("/api/removeStudentFromGroup")
    def http_get_api_removeStudentFromGroup(self, handler):
        q = VPLHTTPServer.query_param(handler)
        if "name" not in q:
            return VPLHTTPServer.error("Missing name")
        return self.call_api(Db.remove_student_from_group,
                             q["name"][0])

    @http_get("/api/listGroupStudents")
    def http_get_api_listGroupStudents(self, handler):
        q = VPLHTTPServer.query_param(handler)
        if "group" not in q:
            return VPLHTTPServer.error("Missing group")
        return self.call_api(Db.list_group_students,
                             q["group"][0])

    @http_get("/api/beginSession")
    def http_get_api_beginSession(self, handler):
        q = VPLHTTPServer.query_param(handler)
        name = q["name"][0] if "name" in q else None
        group = q["group"][0] if "group" in q else None
        if (name is None and group is None):
            return VPLHTTPServer.error("Missing name and group")
        elif name is not None and group is not None:
            return VPLHTTPServer.error("Both name and group")
        robot = q["robot"][0] if "robot" in q else None
        force = "force" in q and q["force"][0] == "true"
        if name is not None:
            return self.call_api(Db.begin_student_session,
                                 name, robot, force)
        else:
            return self.call_api(Db.begin_group_session,
                                 group, robot, force)

    @http_get("/api/endSession")
    def http_get_api_endSession(self, handler):
        q = VPLHTTPServer.query_param(handler)
        if "session" not in q:
            return VPLHTTPServer.error("Missing session")
        return self.call_api(Db.end_session,
                             q["session"][0])

    @http_get("/api/endAllSessions")
    def http_get_api_endAllSessions(self, handler):
        return self.call_api(Db.end_all_sessions)

    @http_get("/api/listSessions")
    def http_get_api_listSessions(self, handler):
        return self.call_api(Db.list_sessions)

    @http_post("/api/addFile")
    def http_put_api_addFile(self, handler):
        q = VPLHTTPServer.query_param(handler)
        if "filename" not in q:
            return VPLHTTPServer.error("Missing filename")
        content = VPLHTTPServer.get_data(handler)
        return self.call_api(Db.add_file,
                             q["filename"][0],
                             content,
                             q["student"][0]
                             if "student" in q
                             else None,
                             q["group"][0] if "group" in q else None,
                             q["metadata"][0]
                             if "metadata" in q
                             else None)

    @http_get("/api/getFile")
    def http_get_api_getFile(self, handler):
        q = VPLHTTPServer.query_param(handler)
        if "id" not in q:
            return VPLHTTPServer.error("Missing id")
        print(handler.path)
        print(q)
        print(q["id"][0])
        return self.call_api(Db.get_file, int(q["id"][0]))

    @http_post("/api/updateFile")
    def http_get_api_updateFile(self, handler):
        q = VPLHTTPServer.query_param(handler)
        if "id" not in q:
            return VPLHTTPServer.error("Missing id")
        content = VPLHTTPServer.get_data(handler)
        return self.call_api(Db.update_file,
                             int(q["id"][0]), content)

    @http_get("/api/removeFiles")
    def http_get_api_removeFiles(self, handler):
        q = VPLHTTPServer.query_param(handler)
        if "id" not in q:
            return VPLHTTPServer.error("Missing id")
        idList = list(map(int, q["id"][0].split(" ")))
        return self.call_api(Db.remove_files, idList)

    @http_get("/api/listFiles")
    def http_get_api_listFiles(self, handler):
        q = VPLHTTPServer.query_param(handler)
        student = q["student"][0] if "student" in q else None
        last = q["last"][0].lower() == "true" if "last" in q else False
        return self.call_api(Db.list_files,
                             student=student,
                             last=last)

    @http_get("/api/getLog")
    def http_get_api_getLog(self, handler):
        q = VPLHTTPServer.query_param(handler)
        id = q["id"][0] if "id" in q else None
        last = q["last"][0] if "last" in q else None
        return self.call_api(Db.get_log, session_id=id, last_of_type=last)

    @http_get("/api/shortenURL")
    def http_get_api_shortenURL(self, handler):
        q = VPLHTTPServer.query_param(handler)
        if "u" in q:
            return {
                "mime": "text/plain",
                "data": f"http://{URLUtil.get_local_IP()}:{self.http_port}/xx{self.url_shortcuts.add(q['u'][0])}\n"
            }
        else:
            return VPLHTTPServer.error("missing url")

    @http_get_any
    def http_get_shortenedURL(path, self, handler):
        if path.startswith("/xx"):
            key = path[3:]
            url = self.url_shortcuts.get(key)
            if url is not None:
                return {
                    "location": url
                }
            else:
                return VPLHTTPServer.error("unknown shortcut")


if __name__ == "__main__":
    port = VPLHTTPServer.DEFAULT_PORT
    try:
        arguments, values = getopt.getopt(sys.argv[1:],
                                          "", ["help", "port=", "link="])
    except getopt.error as err:
        print(str(err))
        sys.exit(1)
    for arg, val in arguments:
        if arg == "--help":
            print(f"""Usage: {sys.argv[0]} options
VPL 3 teacher tools http server

Options:
  --help     display help message and exit
  --port num http server port number (default: {VPLHTTPServer.DEFAULT_PORT})
            """)
            sys.exit(0)
        elif arg == "--port":
            port = int(val)

    server = VPLHTTPServer(http_port=port, logger=print)
    server.run()
