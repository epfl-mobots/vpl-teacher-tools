"""
This is a setup.py script generated by py2applet and modified for vpl3

Usage:
    python setup.py py2app
"""

from setuptools import setup

APPNAME = "VPL3Server"
VERSION = "0.1"
URL = "http://mobots.epfl.ch"
AUTHOR = "Yves Piguet"
AUTHOR_EMAIL = "yves dot piguet a epfl dot CH"
APP = ['launch_objc.py']
DATA_FILES = [
    ("", ["vpl3tt/data"]),
    ("", ["vpl3tt/data/behaviors"]),
    ("", ["vpl3tt/doc"]),
]
OPTIONS = {
    # list of module names as used by import statements
    # beware! "pip install websocket-client" for module websocket
    "packages": "sqlite3,tkinter,websockets,websocket,qrcode,thymiodirect",
    "dist_dir": ".",
    "excludes": [
        "debugpy",
        "ipykernel",
        "IPython",
        "numpy",
        "wx",
        "zmq",
    ],
    "plist": {
        "CFBundleIdentifier": "ch.epfl.mobots.vpl3server",
        "CFBundleVersion": "0.1",
        "NSHumanReadableCopyright":
            "2019-2021, École polytechnique fédérale de Lausanne (EPFL)",
    }
}

setup(
    name=APPNAME,
    version=VERSION,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
