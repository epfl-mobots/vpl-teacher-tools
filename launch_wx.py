#!/usr/bin/python3

# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# server app launcher with wx user interface

from vpl3.launch import launch
from vpl3.wxapp import Application

if __name__ == "__main__":
    launch(Application)
