#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# Path of resources in package

import os


class DataPath:

    @staticmethod
    def path(relative_path):
        """Get the absolute path of a file or directory specified by a path
        relative to the parent directory of __file__.
        """
        abs_path = os.path.join(os.path.split(__file__)[0], relative_path)
        return abs_path
