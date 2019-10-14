# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

"""Class Db"""

import sqlite3
import os
import re
import itertools


class Db:
    """
    Interface to VPL database
    """

    DEFAULT_PATH = os.path.expanduser("~/vpl.sqlite")

    LOCAL_TIME = True

    ORDER_TIME = "time"
    ORDER_FILENAME = "filename"

    def __init__(self, path=None):
        self.path = path if path is not None else self.DEFAULT_PATH
        self._db = sqlite3.connect(self.path)

        # create all tables if they don't exist yet
        sql = [
            """
            CREATE TABLE IF NOT EXISTS students (
                studentid INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                time TEXT DEFAULT CURRENT_TIMESTAMP,
                groupid INTEGER
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS groups (
                groupid INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                time TEXT DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS membership (
                studentid INTEGER,
                groupid INTEGER,
                begintime TEXT,
                endtime TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS files (
                fileid INTEGER PRIMARY KEY AUTOINCREMENT,
                studentid INTEGER,
                groupid INTEGER,
                name TEXT,
                time TEXT DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT,
                content TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS log (
                studentid INTEGER,
                groupid INTEGER,
                type TEXT,
                time TEXT DEFAULT CURRENT_TIMESTAMP,
                data TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS sessions (
                studentid INTEGER,
                groupid INTEGER,
                special TEXT,
                sessionid TEXT UNIQUE,
                time TEXT DEFAULT CURRENT_TIMESTAMP,
                robot TEXT
            );
            """
        ]
        c = self._db.cursor()
        for statement in sql:
            c.execute(statement)

        # "session id": (studentid, groupid)
        self.session_cache = {}

    def __del__(self):
        self._db.close()

    @staticmethod
    def remove(path=None):
        """Remove the SQLite database"""
        os.remove(path if path is not None else Db.DEFAULT_PATH)

    def get_first_result(self, select, from_table, where, *args):
        """Get the first result of an SQL query as a tupple"""
        c = self._db.cursor()
        c.execute("SELECT " + select + " FROM " + from_table
                  + " WHERE " + where + " LIMIT 1",
                  *args)
        return c.fetchone()

    def select_has_result(self, from_table, where, *args):
        """Check if the result of an SQL query has at least one result"""
        c = self._db.cursor()
        c.execute("SELECT 1 FROM " + from_table
                  + " WHERE " + where + " LIMIT 1",
                  *args)
        return c.fetchone() is not None

    def delete_all_students(self):
        """Delete all students and groups"""
        c = self._db.cursor()
        c.execute("""
            DELETE FROM students
        """)
        c.execute("""
            DELETE FROM groups
        """)
        self._db.commit()

    def add_student(self, name):
        """Add a new student"""
        if self.select_has_result("students", "name=?", (name,)):
            raise ValueError("duplicate student")
        c = self._db.cursor()
        c.execute("INSERT INTO students (name) VALUES (?)", (name,))
        self._db.commit()

    def list_students(self):
        """Get a list of all students"""
        c = self._db.cursor()
        c.execute(f"""
            SELECT name,
                   {"datetime(time,'localtime')" if Db.ORDER_TIME else "time"},
                   (SELECT name
                    FROM groups
                    WHERE groups.groupid = students.groupid)
            FROM students
        """)
        return [
            {"name": row[0], "time": row[1], "group": row[2]}
            for row in c.fetchall()
        ]

    def remove_student(self, name):
        """Remove a student"""
        if not self.select_has_result("students", "name=?", (name,)):
            raise ValueError("student not found")
        c = self._db.cursor()
        c.execute("DELETE FROM students WHERE name=?", (name,))
        self._db.commit()

    def add_group(self, group):
        """Add a new group"""
        if self.select_has_result("groups", "name=?", (group,)):
            raise ValueError("duplicate group")
        c = self._db.cursor()
        c.execute("INSERT INTO groups (name) VALUES (?)", (group,))
        self._db.commit()

    def list_groups(self):
        """Get the list of all groups"""
        c = self._db.cursor()
        c.execute(f"""
            SELECT name,
                   {"datetime(time,'localtime')" if Db.ORDER_TIME else "time"},
                   (SELECT count()
                    FROM students
                    WHERE students.groupid = groups.groupid)
            FROM groups
        """)
        return [
            {"name": row[0], "time": row[1], "numStudents": row[2]}
            for row in c.fetchall()
        ]

    def remove_group(self, group):
        """Remove a group"""
        if not self.select_has_result("groups", "name=?", (group,)):
            raise ValueError("group not found")
        c = self._db.cursor()
        c.execute("DELETE FROM groups WHERE name=?", (group,))
        self._db.commit()

    def add_student_to_group(self, name, group):
        """Add an existing student to a group (or change group)"""
        r = self.get_first_result("groupid", "groups", "name=?",
                                  (group,))
        if r is None:
            raise ValueError("group not found")
        group_id = r[0]
        r = self.get_first_result("groupid", "students", "name=?", (name,))
        if r is None:
            raise ValueError("student not found")
        membership = r[0]
        if membership != group_id:
            c = self._db.cursor()
            if membership is not None:
                c.execute("""
                    UPDATE membership
                    SET endtime = datetime('now')
                    WHERE groupid=?
                        AND studentid
                            = (SELECT studentid FROM students WHERE name=?)
                    ORDER BY julianday(begintime) DESC
                    LIMIT 1
                """, (group_id, name))
            c.execute("""
                INSERT INTO membership (studentid, groupid, begintime)
                VALUES (
                    (SELECT studentid FROM students WHERE name=?),
                    ?,
                    datetime('now')
                )
            """, (name, group_id))
            c.execute("""
                UPDATE students
                SET groupid = ?
                WHERE name = ?
            """, (group_id, name))
            self._db.commit()

    def remove_student_from_group(self, name):
        """Remove a student from her group"""
        r = self.get_first_result("groupid", "students", "name=?",
                                  (name,))
        if r is None:
            raise ValueError("student not found")
        group_id = r[0]
        if group_id is not None:
            c = self._db.cursor()
            c.execute("""
                UPDATE membership
                SET endtime = datetime('now')
                WHERE groupid=?
                    AND studentid=(SELECT studentid FROM students WHERE name=?)
                ORDER BY julianday(begintime) DESC
                LIMIT 1
            """, (group_id, name))
            c.execute("""
                UPDATE students
                SET groupid = NULL
                WHERE name=?
            """, (name,))
            self._db.commit()

    def list_group_students(self, group):
        """Get a list of all students belonging to a group"""
        c = self._db.cursor()
        c.execute("""
                    SELECT name
                    FROM students
                    WHERE groupid = (SELECT groupid FROM groups WHERE name=?)
                  """,
                  (group,))
        return [row[0] for row in c.fetchall()]

    def begin_session(self, student_id, group_id, special, robot, force):
        c = self._db.cursor()
        if student_id is not None:
            if self.select_has_result("sessions", "studentid=?",
                                      (student_id,)):
                if force:
                    c.execute("DELETE FROM sessions WHERE studentid=?",
                              (student_id,))
                else:
                    raise ValueError("session already open for student")
        elif group_id is not None:
            if self.select_has_result("sessions", "groupid=?",
                                      (group_id,)):
                if force:
                    c.execute("DELETE FROM sessions WHERE groupid=?",
                              (group_id,))
                else:
                    raise ValueError("session already open for group")
        elif special is None:
            raise ValueError("begin session argument error")
        if not robot.startswith("!"):
            if self.select_has_result("sessions", "robot=?",
                                      (robot,)):
                if force:
                    c.execute("DELETE FROM sessions WHERE robot=?",
                              (robot,))
                else:
                    raise ValueError("robot already used")
        c.execute("""
            INSERT INTO sessions (studentid,groupid,special,robot,sessionid)
            VALUES (?,?,?,?,lower(hex(randomblob(16))))
        """, (student_id, group_id, special, robot))
        rowid = c.lastrowid
        self._db.commit()
        session_id = self.get_first_result("sessionid", "sessions", "rowid=?",
                                           (rowid,))[0]
        self.session_cache[session_id] = (student_id, group_id)
        return session_id

    def end_session(self, session_id):
        if not self.select_has_result("sessions", "sessionid=?",
                                      (session_id,)):
            raise ValueError("session id not found")
        c = self._db.cursor()
        c.execute("DELETE FROM sessions WHERE sessionid=?", (session_id,))
        self._db.commit()
        if session_id in self.session_cache:
            del self.session_cache[session_id]

    def end_all_sessions(self):
        c = self._db.cursor()
        c.execute("DELETE FROM sessions")
        self._db.commit()
        self.session_cache = {}

    def get_session(self, session_id):
        if session_id in self.session_cache:
            return self.session_cache[session_id]

        r = self.get_first_result("studentid,groupid,special", "sessions",
                                  "sessionid=?", (session_id,))
        if r is None:
            raise ValueError("session id not found")
        self.session_cache[session_id] = r
        return r

    def list_sessions(self):
        """Get a list of all sessions"""
        c = self._db.cursor()
        c.execute("""
            SELECT
                sessionid,
                (SELECT name
                    FROM students
                    WHERE students.studentid = sessions.studentid)
                    AS student,
                (SELECT name
                    FROM groups
                    WHERE groups.groupid = sessions.groupid)
                    AS groupname,
                special,
                robot
            FROM sessions
        """)

        return [
            {
                "session_id": row[0],
                "student": row[1],
                "group": row[2],
                "special": row[3],
                "robot": row[4]
            } for row in c.fetchall()
        ]

    def begin_student_session(self, name, robot, force):
        """Begin a session for a student"""
        if name.startswith("!"):
            return self.begin_session(None, None, name, robot, force)
        else:
            r = self.get_first_result("studentid,groupid",
                                      "students", "name=?",
                                      (name,))
            if r is None:
                raise ValueError("student not found")
            student_id = r[0]
            group_id = r[1]
            return self.begin_session(student_id if group_id is None else None,
                                      group_id, None, robot, force)

    def begin_group_session(self, group, robot, force):
        """Begin a session for a group"""
        if group.startswith("!"):
            return self.begin_session(None, None, group, robot, force)
        else:
            r = self.get_first_result("groupid", "groups", "name=?",
                                      (group,))
            if r is None:
                raise ValueError("group not found")
            group_id = r[0]
            return self.begin_session(None, group_id, None, robot, force)

    def add_log(self, session_id, type, data=""):
        print("add_log session_id=" + session_id)
        r = self.get_session(session_id)
        if r[2] is None or not r[2].startswith("!"):
            print(f"will log data='{data}' for r='{r}'")
            c = self._db.cursor()
            c.execute("""
                INSERT INTO log (studentid, groupid, type, data)
                VALUES (?,?,?,?)
            """, (r[0], r[1], type, data))
            self._db.commit()
        else:
            print("oops, add_log's session_id not found")
            print(r)

    def get_log(self, session_id, last_of_type=None):
        r = self.get_session(session_id)
        group_id = r[1]
        c = self._db.cursor()
        if last_of_type:
            c.execute(f"""
                SELECT type,
                       {"datetime(time,'localtime')"
                        if Db.ORDER_TIME
                        else "time"},
                       data
                FROM log
                WHERE groupid IS ? AND type == ?
                ORDER BY time DESC
            """, (group_id, last_of_type))
            row = c.fetchone()
            return [
                {
                    "type": row[0],
                    "time": row[1],
                    "data": row[2]
                }
            ] if row is not None else []
        else:
            c.execute(f"""
                SELECT type,
                       {"datetime(time,'localtime')"
                        if Db.ORDER_TIME
                        else "time"},
                       data
                FROM log
                WHERE groupid IS ?
                ORDER BY time DESC
            """, (group_id,))
            return [
                {
                    "type": row[0],
                    "time": row[1],
                    "data": row[2]
                }
                for row in c.fetchall()
            ]

    def add_file(self, filename, content,
                 student=None, group=None, metadata=None):
        """Add a file"""
        student_id = None
        group_id = None
        if student:
            print(student)
            r = self.get_first_result("studentid,groupid",
                                      "students", "name=?",
                                      (student,))
            if r is None:
                raise ValueError("student not found")
            student_id = r[0]
            group_id = r[1]
        elif group:
            r = self.get_first_result("groupid", "groups", "name=?",
                                      (group,))
            if r is None:
                raise ValueError("group not found")
            group_id = r[0]
        c = self._db.cursor()
        c.execute("""
            INSERT
            INTO files (name, content, studentid, groupid, metadata)
            VALUES (?,?,?,?,?)
        """, (filename, content, student_id, group_id, metadata))
        self._db.commit()
        rowid = c.lastrowid
        file_id = self.get_first_result("fileid", "files", "rowid=?",
                                        (rowid,))[0]
        return file_id

    def update_file(self, file_id, content):
        """Replace file content"""
        c = self._db.cursor()
        c.execute("""
            UPDATE files
            SET time=CURRENT_TIMESTAMP, content=?
            WHERE fileid=?
        """, (content, file_id))
        self._db.commit()

    def remove_files(self, file_id_list):
        """Remove files"""
        c = self._db.cursor()
        for file_id in file_id_list:
            if not self.select_has_result("files", "fileid=?", (file_id,)):
                raise ValueError("file id not found")
            c.execute("DELETE FROM files WHERE fileid=?", (file_id,))
        self._db.commit()

    def get_file(self, file_id):
        r = self.get_first_result(
            f"""name,
                {"datetime(time,'localtime')" if Db.ORDER_TIME else "time"},
                LENGTH(content),
                studentid,
                groupid,
                content,
                metadata
            """,
            "files",
            "fileid=?", (file_id,))
        if r is None:
            raise ValueError("file id not found")
        return {
            "id": file_id,
            "filename": r[0],
            "time": r[1],
            "size": r[2],
            "student_id": r[3],
            "group_id": r[4],
            "content": r[5],
            "metadata": r[6]
        }

    def list_files(self,
                   filename=None, student=None, group=None,
                   order=None,
                   last=False):
        """Get a list of files, optionnally filtering, ordering and last"""
        order = order or (Db.ORDER_FILENAME if last else Db.ORDER_TIME)
        c = self._db.cursor()
        student_id = None
        group_id = None
        if student:
            r = self.get_first_result("studentid,groupid",
                                      "students", "name=?",
                                      (student,))
            if r is None:
                raise ValueError("student not found")
            student_id = re.sub("[^0-9]", "", r[0])  # sanitizd b/c ins in sql
            group_id = re.sub("[^0-9]", "", r[1])  # sanitizd b/c ins in sql
        if group:
            r = self.get_first_result("groupid",
                                      "groups", "name=?",
                                      (group,))
            if r is None:
                raise ValueError("group not found")
            group_id = r[0]
        sql = f"""
            SELECT fileid, name,
                   {"datetime(time,'localtime')" if Db.ORDER_TIME else "time"},
                   LENGTH(content),
                   metadata,
                   (SELECT name
                    FROM students
                    WHERE students.studentid = files.studentid) AS studentname,
                   (SELECT name
                    FROM groups
                    WHERE groups.groupid = files.groupid) AS groupname
            FROM files
            WHERE 1
                {
                    "AND files.studentid IS NULL"
                    if student == "" else
                    "AND (files.studentid = " + str(student_id)
                        + " OR files.groupid = " + str(group_id)
                        + ")"
                    if student is not None else ""
                }
                {
                    "AND files.groupid IS NULL"
                    if group == "" else
                    "AND files.groupid = " + str(group_id)
                    if group is not None else ""
                }
            ORDER BY {
                "fileid DESC" if order is Db.ORDER_TIME
                else "name ASC, studentname ASC, groupname ASC, fileid DESC"
            }
        """
        c.execute(sql)
        if last:
            xx = [
                next(group) for key, group in itertools.groupby(({
                        "id": row[0],
                        "filename": row[1],
                        "time": row[2],
                        "size": row[3],
                        "metadata": row[4],
                        "student": row[5],
                        "group": row[6]
                    } for row in c.fetchall()),
                    key=lambda e: (e["filename"], e["student"], e["group"]))
            ]
            # print(xx)
            return xx
        else:
            return [
                {
                    "id": row[0],
                    "filename": row[1],
                    "time": row[2],
                    "size": row[3],
                    "metadata": row[4],
                    "student": row[5],
                    "group": row[6]
                }
                for row in c.fetchall()
            ]
