# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

"""Class Db"""

import sqlite3
import os
import re
import itertools
import json


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
        self.new_db = not os.path.exists(self.path)
        self._db = sqlite3.connect(self.path)

        # custom functions

        def fun_list_doesinclude(l, i):
            """True if number in arg 2 is included in comma-separated list string in arg 1"""
            return l and i in {int(el) for el in l.split(",")}

        def fun_list_aredisjoint(l1, l2):
            """True if comma-separated list strings have no common element"""
            if not l1 or not l2:
                return True
            a1 = {int(el) for el in l1.split(",")}
            a2 = {int(el) for el in l2.split(",")}
            return a1.isdisjoint(a2)

        def fun_equal_ic(str1, str2):
            """True if strings are equal, ignoring case"""
            return str1.casefold() == str2.casefold()

        if self.new_db:
            self.create_tables()
        else:
            self.upgrade_tables()

        self._db.create_function("list_doesinclude", 2, fun_list_doesinclude)
        self._db.create_function("list_aredisjoint", 2, fun_list_aredisjoint)
        self._db.create_function("equal_ic", 2, fun_equal_ic)

        # "session id": groupid
        self.session_cache = {}

    def __del__(self):
        self._db.close()

    def create_tables(self):
        """Create all tables if they don't exist yet"""

        sql = [
            """
            CREATE TABLE IF NOT EXISTS students (
                studentid INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                time TEXT DEFAULT CURRENT_TIMESTAMP,
                groupid INTEGER
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS groups (
                groupid INTEGER PRIMARY KEY,
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
                fileid INTEGER PRIMARY KEY,
                owner TEXT,
                name TEXT,
                time TEXT DEFAULT CURRENT_TIMESTAMP,
                mark INTEGER DEFAULT 0,
                defaul INTEGER DEFAULT 0,
                metadata TEXT,
                content TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS log (
                owner TEXT,
                type TEXT,
                time TEXT DEFAULT CURRENT_TIMESTAMP,
                data TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS sessions (
                groupid INTEGER,
                sessionid TEXT UNIQUE,
                time TEXT DEFAULT CURRENT_TIMESTAMP,
                robot TEXT
            );
            """
        ]
        c = self._db.cursor()
        for statement in sql:
            c.execute(statement)
        self._db.commit()

    def upgrade_tables(self):
        """Upgrade tables"""

        sql = [
            """
            CREATE TEMPORARY TABLE groups_backup(
                groupid INTEGER PRIMARY KEY,
                time TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            INSERT INTO groups_backup (groupid, time)
            SELECT groupid, time FROM groups
            """,
            """
            DROP TABLE groups
            """,
            """
            CREATE TABLE groups(
                groupid INTEGER PRIMARY KEY,
                time TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            INSERT INTO groups (groupid, time)
            SELECT groupid, time FROM groups_backup
            """,
            """
            DROP TABLE groups_backup
            """
        ]
        # c = self._db.cursor()
        # for statement in sql:
        #     c.execute(statement)
        # self._db.commit()

    @staticmethod
    def remove(path=None):
        """Remove the SQLite database"""
        os.remove(path if path is not None else Db.DEFAULT_PATH)

    def get_first_result(self, select, from_table, where, *args, order=None):
        """Get the first result of an SQL query as a tupple"""
        c = self._db.cursor()
        try:
            c.execute("SELECT " + select + " FROM " + from_table
                      + " WHERE " + where
                      + (" ORDER BY " + order if order else "")
                      + " LIMIT 1",
                      *args)
        finally:
            self._db.commit()
        return c.fetchone()

    def select_has_result(self, from_table, where, *args):
        """Check if the result of an SQL query has at least one result"""
        c = self._db.cursor()
        try:
            c.execute("SELECT 1 FROM " + from_table
                      + " WHERE " + where + " LIMIT 1",
                      *args)
        finally:
            self._db.commit()
        return c.fetchone() is not None

    def list_to_str(self, list_of_id):
        return ",".join([str(id) for id in list_of_id])

    def str_to_list(self, str):
        return list({int(el) for el in str.split(",")}) if str else []

    def get_student_id(self, name):
        r = self.get_first_result("studentid", "students", "equal_ic(name,?)", (name,))
        if r is None:
            raise ValueError("student not found")
        return r[0]

    def get_student_name(self, student_id):
        r = self.get_first_result("name", "students", "studentid=?", (student_id,))
        if r is None:
            raise ValueError("student id not found")
        return r[0]

    def delete_all_students(self):
        """Delete all students and groups"""
        c = self._db.cursor()
        try:
            c.execute("""
                DELETE FROM students
            """)
            c.execute("""
                DELETE FROM groups
            """)
        finally:
            self._db.commit()

    def add_student(self, name):
        """Add a new student"""
        if self.select_has_result("students", "equal_ic(name,?)", (name,)):
            raise ValueError("duplicate student")
        c = self._db.cursor()
        try:
            c.execute("INSERT INTO students (name) VALUES (?)", (name,))
        finally:
            self._db.commit()

    def add_students(self, name_list):
        """Add multiple students, ignoring existing ones"""
        c = self._db.cursor()
        try:
            for name in name_list:
                c.execute("""
                    INSERT INTO students (name)
                    SELECT ?
                    WHERE NOT EXISTS(SELECT name FROM students WHERE name = ?)
                """, (name, name))
        finally:
            self._db.commit()

    def list_students(self):
        """Get a list of all students"""
        c = self._db.cursor()
        try:
            c.execute(f"""
                SELECT name,
                       studentid,
                       {"datetime(time,'localtime')" if Db.ORDER_TIME else "time"},
                       groupid
                FROM students
            """)
        finally:
            self._db.commit()
        return [
            {
                "name": row[0],
                "student_id": row[1],
                "time": row[2],
                "group_id": row[3]
            }
            for row in c.fetchall()
        ]

    def remove_student(self, name):
        """Remove a student"""
        if not self.select_has_result("students", "equal_ic(name,?)", (name,)):
            raise ValueError("student not found")
        c = self._db.cursor()
        try:
            c.execute("DELETE FROM students WHERE equal_ic(name,?)", (name,))
        finally:
            self._db.commit()

    def add_group(self, student_name=None):
        """Create a new group, optionally with a student, and return its id"""
        c = self._db.cursor()
        try:
            c.execute("INSERT INTO groups DEFAULT VALUES")
            group_id = c.lastrowid
            self._db.commit()
            if student_name is not None:
                self.add_student_to_group(student_name, group_id)
        finally:
            self._db.commit()
        return group_id

    def list_groups(self):
        """Get the list of all groups"""
        c = self._db.cursor()
        try:
            c.execute(f"""
                SELECT groupid,
                       {"datetime(time,'localtime')" if Db.ORDER_TIME else "time"},
                       (SELECT count()
                        FROM students
                        WHERE students.groupid = groups.groupid),
                       (SELECT sessionid
                        FROM sessions
                        WHERE sessions.groupid = groups.groupid
                        LIMIT 1),
                       (SELECT robot
                        FROM sessions
                        WHERE sessions.groupid = groups.groupid
                        LIMIT 1)
                FROM groups
            """)
        finally:
            self._db.commit()
        return [
            {
                "group_id": row[0],
                "time": row[1],
                "numStudents": row[2],
                "session_id": row[3],
                "robot": row[4]
            } for row in c.fetchall()
        ]

    def remove_group(self, group_id):
        """Remove a group"""
        if not self.select_has_result("groups", "groupid=?", (group_id,)):
            raise ValueError("group id not found")
        c = self._db.cursor()
        try:
            c.execute("DELETE FROM groups WHERE groupid=?", (group_id,))
        finally:
            self._db.commit()

    def end_membership(self, group_id, student_name):
        """Update membership table to end a membership now"""
        student_id = self.get_student_id(student_name)
        r = self.get_first_result("rowid", "membership",
                                  "studentid=? AND groupid=?",
                                  (student_id, group_id),
                                  order="julianday(begintime) DESC")
        if r is None:
            raise ValueError("membership not found")
        row_id = r[0]
        c = self._db.cursor()
        try:
            c.execute("""
                UPDATE membership
                SET endtime = datetime('now')
                WHERE rowid=?
            """, (row_id,))
        finally:
            self._db.commit()

    def add_student_to_group(self, student_name, group_id):
        """Add an existing student to a group (or change group)"""
        r = self.get_first_result("groupid", "students", "equal_ic(name,?)", (student_name,))
        if r is None:
            raise ValueError("student not found")
        membership = r[0]
        if membership != group_id:
            if membership is not None:
                self.end_membership(membership, student_name)
            c = self._db.cursor()
            try:
                c.execute("""
                    INSERT INTO membership (studentid, groupid, begintime)
                    VALUES (
                        (SELECT studentid FROM students WHERE equal_ic(name,?)),
                        ?,
                        datetime('now')
                    )
                """, (student_name, group_id))
                c.execute("""
                    UPDATE students
                    SET groupid = ?
                    WHERE name = ?
                """, (group_id, student_name))
            finally:
                self._db.commit()

            # remove previous group if empty
            if membership is not None:
                try:
                    c.execute("""
                        SELECT count(*)
                        FROM students
                        WHERE groupid=?
                              """, (membership,))
                    num_students_left = int(c.fetchone()[0])
                    if num_students_left == 0:
                        c.execute("DELETE FROM groups WHERE groupid=?",
                                  (membership,))
                finally:
                    self._db.commit()

    def remove_student_from_group(self, student_name):
        """Remove a student from her group, and the group itself if empty"""
        r = self.get_first_result("groupid", "students", "equal_ic(name,?)",
                                  (student_name,))
        if r is None:
            raise ValueError("student not found")
        group_id = r[0]
        if group_id is not None:
            self.end_membership(group_id, student_name)
            c = self._db.cursor()
            try:
                c.execute("""
                    UPDATE students
                    SET groupid = NULL
                    WHERE equal_ic(name,?)
                """, (student_name,))
            finally:
                self._db.commit()

            # remove group if empty
            try:
                c.execute("""
                    SELECT count(*)
                    FROM students
                    WHERE groupid=?
                          """, (group_id,))
                num_students_left = int(c.fetchone()[0])
                if num_students_left == 0:
                    c.execute("DELETE FROM groups WHERE groupid=?", (group_id,))
            finally:
                self._db.commit()

    def list_group_students(self, group_id):
        """Get a list of all students belonging to a group"""
        c = self._db.cursor()
        try:
            c.execute("""
                        SELECT name
                        FROM students
                        WHERE groupid = ?
                      """,
                      (group_id,))
        finally:
            self._db.commit()

        return [row[0] for row in c.fetchall()]

    def begin_session(self, group_id, robot, force):
        c = self._db.cursor()
        if self.select_has_result("sessions", "groupid=?",
                                  (group_id,)):
            if force:
                c.execute("DELETE FROM sessions WHERE groupid=?",
                          (group_id,))
            else:
                raise ValueError("session already open for group")
        if not robot.startswith("!"):
            if self.select_has_result("sessions", "robot=?",
                                      (robot,)):
                if force:
                    c.execute("DELETE FROM sessions WHERE robot=?",
                              (robot,))
                else:
                    raise ValueError("robot already used")
        try:
            c.execute("""
                INSERT INTO sessions (groupid,robot,sessionid)
                VALUES (?,?,lower(hex(randomblob(16))))
            """, (group_id, robot))
            rowid = c.lastrowid
            session_id = self.get_first_result("sessionid", "sessions", "rowid=?",
                                               (rowid,))[0]
            self.session_cache[session_id] = group_id
        finally:
            self._db.commit()
        return session_id

    def end_session(self, session_id):
        if not self.select_has_result("sessions", "sessionid=?",
                                      (session_id,)):
            raise ValueError("session id not found")
        c = self._db.cursor()
        try:
            c.execute("DELETE FROM sessions WHERE sessionid=?", (session_id,))
        finally:
            self._db.commit()
        if session_id in self.session_cache:
            del self.session_cache[session_id]

    def end_all_sessions(self):
        c = self._db.cursor()
        try:
            c.execute("DELETE FROM sessions")
        finally:
            self._db.commit()
        self.session_cache = {}

    def get_session_group_id(self, session_id):
        if session_id in self.session_cache:
            return self.session_cache[session_id]

        r = self.get_first_result("groupid", "sessions",
                                  "sessionid=?", (session_id,))
        if r is None:
            raise ValueError("session id not found")
        self.session_cache[session_id] = r[0]
        return r[0]

    def get_session_student_names(self, session_id):
        group_id = self.get_session_group_id(session_id)
        c = self._db.cursor()
        try:
            c.execute("SELECT name FROM students WHERE groupid=?", (group_id,))
            return [r[0] for r in c.fetchall()]
        finally:
            self._db.commit()

    def list_sessions(self):
        """Get a list of all sessions"""
        c = self._db.cursor()
        try:
            c.execute("""
                SELECT
                    sessionid,
                    groupid,
                    robot
                FROM sessions
            """)

            return [
                {
                    "session_id": row[0],
                    "group_id": row[1],
                    "robot": row[2]
                } for row in c.fetchall()
            ]
        finally:
            self._db.commit()

    def get_group_student_list(self, group_id):
        c = self._db.cursor()
        try:
            c.execute("""
                SELECT studentid
                FROM students
                WHERE groupid=?
            """, (group_id,))
            return [row[0] for row in c.fetchall()]
        finally:
            self._db.commit()

    def add_log(self, session_id, type, data=""):
        group_id = self.get_session_group_id(session_id)
        owner = self.list_to_str(self.get_group_student_list(group_id))
        c = self._db.cursor()
        try:
            c.execute("""
                INSERT INTO log (owner, type, data)
                VALUES (?,?,?)
            """, (owner, type, data))
        finally:
            self._db.commit()

    def get_log(self, session_id=None, last_of_type=None):
        group_id = None
        if session_id is not None:
            group_id = self.get_session_group_id(session_id)
            student_id_list = self.list_to_str(self.get_group_student_list(group_id))
        c = self._db.cursor()
        try:
            if last_of_type:
                if group_id is None:
                    c.execute(f"""
                        SELECT type,
                               {"datetime(time,'localtime')"
                                if Db.ORDER_TIME
                                else "time"},
                               owner,
                               data
                        FROM log
                        WHERE type == ?
                        ORDER BY time DESC
                    """, (last_of_type,))
                else:
                    c.execute(f"""
                        SELECT type,
                               {"datetime(time,'localtime')"
                                if Db.ORDER_TIME
                                else "time"},
                               owner,
                               data
                        FROM log
                        WHERE NOT list_aredisjoint(owner, ?) AND type == ?
                        ORDER BY time DESC
                    """, (student_id_list, last_of_type))
                row = c.fetchone()
                return [
                    {
                        "type": row[0],
                        "time": row[1],
                        "owner": row[2],
                        "data": row[3]
                    }
                ] if row is not None else []
            else:
                if group_id is not None:
                    c.execute(f"""
                        SELECT type,
                               {"datetime(time,'localtime')"
                                if Db.ORDER_TIME
                                else "time"},
                               owner,
                               data
                        FROM log
                        WHERE groupid IS ?
                        ORDER BY time DESC
                    """, (group_id,))
                else:
                    c.execute(f"""
                        SELECT type,
                               {"datetime(time,'localtime')"
                                if Db.ORDER_TIME
                                else "time"},
                               owner,
                               data
                        FROM log
                        ORDER BY time DESC
                    """)
                return [
                    {
                        "type": row[0],
                        "time": row[1],
                        "owner": row[2],
                        "data": row[3]
                    }
                    for row in c.fetchall()
                ]
        finally:
            self._db.commit()

    def clear_log(self):
        """Delete all log entries"""
        c = self._db.cursor()
        try:
            c.execute("""
                DELETE FROM log
            """)
        finally:
            self._db.commit()

    def add_file(self, filename, content,
                 group_id=None, metadata=None):
        """Add a file"""
        owner = self.list_to_str(self.get_group_student_list(group_id))
        c = self._db.cursor()
        try:
            c.execute("""
                INSERT
                INTO files (name, content, owner, metadata)
                VALUES (?,?,?,?)
            """, (filename, content, owner, metadata))
        finally:
            self._db.commit()
        rowid = c.lastrowid
        file_id = self.get_first_result("fileid", "files", "rowid=?",
                                        (rowid,))[0]
        return file_id

    def add_local_files(self, path_array):
        for path in path_array:
            filename = os.path.split(path)[-1]
            with open(path, encoding="utf-8") as f:
                content = f.read()
            self.add_file(filename, content)

    def copy_file(self, file_id, filename, mark=False, metadata=None):
        """Copy a file"""
        r = self.get_first_result("content", "files", "fileid=?", (file_id,))
        if r is None:
            raise ValueError("file id not found")
        content = r[0]

        c = self._db.cursor()
        try:
            c.execute("""
                INSERT
                INTO files (name, content, owner, mark, metadata)
                VALUES (?,?,'',?,?)
            """, (filename, content, 1 if mark else 0, metadata))
        finally:
            self._db.commit()
        rowid = c.lastrowid
        file_id = self.get_first_result("fileid", "files", "rowid=?",
                                        (rowid,))[0]
        return file_id

    @staticmethod
    def get_config_from_vpl3(vpl3):
        obj = json.loads(vpl3)
        for prop in ["program", "code"]:
            if prop in obj:
                del obj[prop]
        return json.dumps(obj)

    def extract_config_from_vpl3_file(self, file_id, filename, mark=False, metadata=None):
        """Extract configuration from VPL3 file"""
        r = self.get_first_result("content", "files", "fileid=?", (file_id,))
        if r is None:
            raise ValueError("file id not found")
        content = self.get_config_from_vpl3(r[0])

        c = self._db.cursor()
        try:
            c.execute("""
                INSERT
                INTO files (name, content, owner, mark, metadata)
                VALUES (?,?,'',?,?)
            """, (filename, content, 1 if mark else 0, metadata))
        finally:
            self._db.commit()
        rowid = c.lastrowid
        file_id = self.get_first_result("fileid", "files", "rowid=?",
                                        (rowid,))[0]
        return file_id

    def update_file(self, file_id, content):
        """Replace file content"""
        c = self._db.cursor()
        try:
            c.execute("""
                UPDATE files
                SET time=CURRENT_TIMESTAMP, content=?
                WHERE fileid=?
            """, (content, file_id))
        finally:
            self._db.commit()

    def rename_file(self, file_id, new_filename):
        """Rename file"""
        c = self._db.cursor()
        try:
            c.execute("""
                UPDATE files
                SET name=?
                WHERE fileid=?
            """, (new_filename, file_id))
        finally:
            self._db.commit()

    def mark_file(self, file_id, mark):
        """Set or reset file mark"""
        c = self._db.cursor()
        try:
            c.execute("""
                UPDATE files
                SET mark=?
                WHERE fileid=?
            """, (1 if mark else 0, file_id))
        finally:
            self._db.commit()

    def toggle_file_mark(self, file_id):
        """Toggle file mark"""
        c = self._db.cursor()
        try:
            c.execute("""
                UPDATE files
                SET mark=NOT mark
                WHERE fileid=?
            """, (file_id,))
        finally:
            self._db.commit()

    def set_default_file(self, file_id, suffix=None):
        """Set the default file for the specified extension"""
        c = self._db.cursor()
        try:
            if suffix:
                if suffix[0:1] != ".":
                    suffix = "." + suffix
                c.execute("""
                    UPDATE files
                    SET defaul=fileid=?
                    WHERE substr(name,?)=?
                """, (file_id, -len(suffix), suffix))
            else:
                c.execute("""
                    UPDATE files
                    SET defaul=fileid=?
                """, (file_id,))
        finally:
            self._db.commit()

    def remove_files(self, file_id_list):
        """Remove files"""
        c = self._db.cursor()
        try:
            for file_id in file_id_list:
                if not self.select_has_result("files", "fileid=?", (file_id,)):
                    raise ValueError("file id not found")
                c.execute("DELETE FROM files WHERE fileid=?", (file_id,))
        finally:
            self._db.commit()

    def get_file(self, file_id):
        r = self.get_first_result(
            f"""name,
                {"datetime(time,'localtime')" if Db.ORDER_TIME else "time"},
                LENGTH(content),
                owner,
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
            "owner": self.str_to_list(r[3]),
            "content": r[4],
            "metadata": r[5]
        }

    def get_default_file(self):
        """Get the default file"""
        r = self.get_first_result(
            f"""fileid,
                name,
                {"datetime(time,'localtime')" if Db.ORDER_TIME else "time"},
                LENGTH(content),
                owner,
                content,
                metadata
            """,
            "files",
            "defaul")
        return {
            "id": r[0],
            "filename": r[1],
            "time": r[2],
            "size": r[3],
            "owner": self.str_to_list(r[4]),
            "content": r[5],
            "metadata": r[6]
        } if r else None

    def list_files(self,
                   filename=None, student=None,
                   order=None,
                   last=False):
        """Get a list of files, optionnally filtering, ordering and last;
        student is None for teacher, "*" for any student, or student name"""
        order = order or (Db.ORDER_FILENAME if last else Db.ORDER_TIME)
        c = self._db.cursor()
        try:
            student_id = None
            if student is not None and student != "*":
                r = self.get_first_result("studentid",
                                          "students", "equal_ic(name,?)",
                                          (student,))
                if r is None:
                    raise ValueError("student not found")
                student_id = r[0]
            sql = f"""
                SELECT fileid, name,
                       {"datetime(time,'localtime')" if Db.ORDER_TIME else "time"},
                       LENGTH(content),
                       mark, defaul,
                       metadata,
                       owner
                FROM files
                {
                    "WHERE files.owner = ''" if student is None else
                    "WHERE files.owner != ''" if student == "*" else
                    "WHERE list_doesinclude(files.owner, " + str(student_id) + ")"
                }
                ORDER BY {
                    "fileid DESC" if order is Db.ORDER_TIME
                    else "name ASC, fileid DESC"
                }
            """
            c.execute(sql)
            files = [
                next(group) for key, group in itertools.groupby(({
                        "id": row[0],
                        "filename": row[1],
                        "time": row[2],
                        "size": row[3],
                        "mark": row[4] != 0,
                        "default": row[5] != 0,
                        "metadata": row[6],
                        "owner": row[7]
                    } for row in c.fetchall()),
                    key=lambda e: (e["filename"], e["owner"]))
            ] if last else [
                {
                    "id": row[0],
                    "filename": row[1],
                    "time": row[2],
                    "size": row[3],
                    "mark": row[4] != 0,
                    "default": row[5] != 0,
                    "metadata": row[6],
                    "owner": row[7]
                }
                for row in c.fetchall()
            ]

            # map student ids in owner to student names
            # get all student id->name mappings which will be needed
            student_id_set = set()
            for file in files:
                if file["owner"] is not None:
                    student_id_set |= set(self.str_to_list(file["owner"]))
            student_name_dict = {
                student_id: self.get_student_name(student_id)
                for student_id in student_id_set
            }
            # for each file, convert owner (id list string) to students (name list)
            for file in files:
                file["students"] = (
                    None if file["owner"] is None
                    else [
                        (student_name_dict[student_id] if student_id in student_name_dict else student_id)
                        for student_id in self.str_to_list(file["owner"])
                    ]
                )

            return files
        finally:
            self._db.commit()

    def clear_files(self):
        """Delete all files"""
        c = self._db.cursor()
        try:
            c.execute("""
                DELETE FROM files
            """)
        finally:
            self._db.commit()
