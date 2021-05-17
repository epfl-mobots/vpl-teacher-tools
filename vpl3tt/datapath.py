#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# Path of resources in package

import os
from zipfile import ZipFile


class DataPath:

    @staticmethod
    def path(relative_path, fix_app2py=True):
        """Get the absolute path of a file or directory specified by a path
        relative to the parent directory of __file__.
        """
        abs_path = os.path.join(os.path.split(__file__)[0], relative_path)
        if fix_app2py:
            # replace invalid path in zip file by a path expected directly
            # in the app resources
            # remove lib/python...zip/... before relative_path, if any
            import re
            rel_path_slash = relative_path.replace('\\', '/')
            abs_path = re.sub(f"lib/python[0-9]*.zip/.*/(?={rel_path_slash})",
                              "",
                              abs_path)
        return abs_path

    @staticmethod
    def open(relative_path):

        class ReadableObject:

            def __init__(self, relative_path):
                self.path = DataPath.path(relative_path)
                self.zip = None
                self.f = None

            def __enter__(self):
                if ".zip/" in self.path:
                    zip_file, zip_object = self.path.split(".zip/")
                    zip_file += ".zip"
                    self.zip = ZipFile(zip_file)
                    self.f = self.zip.open(zip_object, mode="rb")
                else:
                    self.f = open(self.path, mode="rb")
                return self.f

            def __exit__(self, exc_type, exc_value, traceback):
                self.f.close()
                if self.zip is not None:
                    self.zip.close()

        return ReadableObject(relative_path)
