"""
This is a setup.py script generated by py2applet and modified for vpl3

Usage:
    python setup.py py2app
"""

from setuptools import setup

APPNAME = "VPL3 Server"
APP = ['launch.py']
DATA_FILES = [
    ("doc",
        [
            "doc/client.js",
            "doc/index.html",
        ]),
    ("doc/libs/qrcodejs",
        [
            "doc/libs/qrcodejs/LICENSE",
            "doc/libs/qrcodejs/qrcode.min.js",
            "doc/libs/qrcodejs/README.md",
        ]),
    ("doc/vpl-teacher-tools",
        [
            "doc/vpl-teacher-tools/dashboard.html",
            "doc/vpl-teacher-tools/dashboard.js",
            "doc/vpl-teacher-tools/doc.html",
            "doc/vpl-teacher-tools/filebrowser.html",
            "doc/vpl-teacher-tools/filebrowser.js",
            "doc/vpl-teacher-tools/html-tools.css",
            "doc/vpl-teacher-tools/initdb-dev.html",
            "doc/vpl-teacher-tools/Logo_vpl.svg",
            "doc/vpl-teacher-tools/ns.js",
            "doc/vpl-teacher-tools/pairing.html",
            "doc/vpl-teacher-tools/pairing.js",
            "doc/vpl-teacher-tools/students.html",
            "doc/vpl-teacher-tools/students.js",
            "doc/vpl-teacher-tools/ui.json",
            "doc/vpl-teacher-tools/util-url.js",
            "doc/vpl-teacher-tools/vpl-about.html",
            "doc/vpl-teacher-tools/vpl.html",
        ]),
    ("doc/vpl",
        [
            "doc/vpl/vpl.html",
            "doc/vpl/EPFL_Logo_SVG.svg",
            "doc/vpl/grs_logo_RGB.svg",
            "doc/vpl/Logo_vpl.svg",
            "doc/vpl/vpl-about.html",
            "doc/vpl/vpl-min.js",
            "doc/vpl/vpl.html",
        ]),
    ("doc/vpl/thymio",
        [
            "doc/vpl/thymio/thymio.js",
        ]),
    ("doc/vpl/ui/classic",
        [
            "doc/vpl/ui/classic/classic.css",
            "doc/vpl/ui/classic/ui.json",
        ]),
    ("doc/vpl/ui/svg",
        [
            "doc/vpl/ui/svg/aseba.json",
            "doc/vpl/ui/svg/Blocks.svg",
            "doc/vpl/ui/svg/buttons.json",
            "doc/vpl/ui/svg/Icons.svg",
            "doc/vpl/ui/svg/js.json",
            "doc/vpl/ui/svg/l2.json",
            "doc/vpl/ui/svg/python.json",
            "doc/vpl/ui/svg/svg.css",
            "doc/vpl/ui/svg/toolbars.json",
            "doc/vpl/ui/svg/ui.json",
        ]),
]
OPTIONS = {
    "packages": "sqlite3,tkinter,websocket,websockets",
    "dist_dir": ".",
    "plist": {
        "CFBundleIdentifier": "ch.epfl.mobots.vpl3-server",
        "CFBundleVersion": "0.1",
        "NSHumanReadableCopyright":
            "2019, École polytechnique fédérale de Lausanne (EPFL)",
    }
}

setup(
    name=APPNAME,
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
