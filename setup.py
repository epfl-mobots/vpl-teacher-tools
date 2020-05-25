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
    ("data",
        [
            "data/basic-sensors.vpl3ui",
            "data/basic-touch.vpl3ui",
            "data/basic-track.vpl3ui",
            "data/simple-sensors.vpl3ui",
            "data/simple-touch.vpl3ui",
            "data/simple-track.vpl3ui",
        ]),
    ("doc",
        [
            "doc/client.js",
            "doc/index.html",
            "doc/login.html",
            "doc/login.fr.html",
            "doc/login-gui.js",
            "doc/tt.html",
            "doc/tt.fr.html",
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
            "doc/vpl-teacher-tools/dashboard.fr.html",
            "doc/vpl-teacher-tools/dashboard-gui.js",
            "doc/vpl-teacher-tools/dashboard.js",
            "doc/vpl-teacher-tools/dev.html",
            "doc/vpl-teacher-tools/dev.fr.html",
            "doc/vpl-teacher-tools/doc.html",
            "doc/vpl-teacher-tools/doc.fr.html",
            "doc/vpl-teacher-tools/filebrowser.html",
            "doc/vpl-teacher-tools/filebrowser.fr.html",
            "doc/vpl-teacher-tools/filebrowser-gui.js",
            "doc/vpl-teacher-tools/filebrowser.js",
            "doc/vpl-teacher-tools/html-tools.css",
        	"doc/vpl-teacher-tools/icon-file-vpl3.svg",
        	"doc/vpl-teacher-tools/icon-file-vpl3ui.svg",
            "doc/vpl-teacher-tools/initdb-dev.html",
            "doc/vpl-teacher-tools/initdb-dev.fr.html",
            "doc/vpl-teacher-tools/initdb-dev-gui.js",
            "doc/vpl-teacher-tools/json-ws-bridge-api.js",
            "doc/vpl-teacher-tools/login.js",
            "doc/vpl-teacher-tools/Logo_vpl.svg",
            "doc/vpl-teacher-tools/ns.js",
            "doc/vpl-teacher-tools/pairing.html",
            "doc/vpl-teacher-tools/pairing.fr.html",
            "doc/vpl-teacher-tools/pairing-gui.js",
            "doc/vpl-teacher-tools/pairing.js",
            "doc/vpl-teacher-tools/robots.js",
            "doc/vpl-teacher-tools/students.html",
            "doc/vpl-teacher-tools/students.fr.html",
            "doc/vpl-teacher-tools/students-gui.js",
            "doc/vpl-teacher-tools/students.js",
            "doc/vpl-teacher-tools/translate.js",
            "doc/vpl-teacher-tools/ui.json",
            "doc/vpl-teacher-tools/util-files.js",
            "doc/vpl-teacher-tools/util-url.js",
            "doc/vpl-teacher-tools/vpl_load.png",
            "doc/vpl-teacher-tools/vpl_new.png",
            "doc/vpl-teacher-tools/vpl_run.png",
            "doc/vpl-teacher-tools/vpl_stop.png",
            "doc/vpl-teacher-tools/vpl-about.html",
            "doc/vpl-teacher-tools/vpl.html",
            "doc/vpl-teacher-tools/vpl.fr.html",
            "doc/vpl-teacher-tools/vpl-gui.js",
            "doc/vpl-teacher-tools/vplurl.js",
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
    ("doc/vpl/ui",
        [
            "doc/vpl/ui/toc.json",
        ]),
    ("doc/vpl/ui/classic",
        [
            "doc/vpl/ui/classic/aesl.json",
            "doc/vpl/ui/classic/aseba.json",
            "doc/vpl/ui/classic/block-english.json",
            "doc/vpl/ui/classic/block-french.json",
            "doc/vpl/ui/classic/classic.css",
            "doc/vpl/ui/classic/cmd-sim-english.json",
            "doc/vpl/ui/classic/cmd-sim-french.json",
            "doc/vpl/ui/classic/cmd-vpl-english.json",
            "doc/vpl/ui/classic/cmd-vpl-french.json",
            "doc/vpl/ui/classic/french.json",
            "doc/vpl/ui/classic/help-blocks-english.json",
            "doc/vpl/ui/classic/help-blocks-french.json",
            "doc/vpl/ui/classic/js.json",
            "doc/vpl/ui/classic/l2.json",
            "doc/vpl/ui/classic/python.json",
            "doc/vpl/ui/classic/typical-param-set.json",
            "doc/vpl/ui/classic/typical-states.json",
            "doc/vpl/ui/classic/ui.json",
        ]),
    ("doc/vpl/ui/svg",
        [
            "doc/vpl/ui/svg/aesl.json",
            "doc/vpl/ui/svg/aseba.json",
            "doc/vpl/ui/svg/block-english.json",
            "doc/vpl/ui/svg/block-french.json",
            "doc/vpl/ui/svg/Blocks16.svg",
            "doc/vpl/ui/svg/Blocks.svg",
            "doc/vpl/ui/svg/buttons.json",
            "doc/vpl/ui/svg/cmd-sim-english.json",
            "doc/vpl/ui/svg/cmd-sim-french.json",
            "doc/vpl/ui/svg/cmd-vpl-english.json",
            "doc/vpl/ui/svg/cmd-vpl-french.json",
            "doc/vpl/ui/svg/french.json",
            "doc/vpl/ui/svg/help-blocks-english.html",
            "doc/vpl/ui/svg/help-blocks-french.html",
            "doc/vpl/ui/svg/Icons.svg",
            "doc/vpl/ui/svg/js.json",
            "doc/vpl/ui/svg/l2.json",
            "doc/vpl/ui/svg/python.json",
            "doc/vpl/ui/svg/svg.css",
            "doc/vpl/ui/svg/toolbars.json",
            "doc/vpl/ui/svg/ui.json",
        ]),
    ("doc/vpl/ui/svg/help",
        [
            "doc/vpl/ui/svg/help/vpl_help.html",
        ]),
    ("doc/vpl/ui/svg/help/images",
        [
            "doc/vpl/ui/svg/help/images/image10.png",
            "doc/vpl/ui/svg/help/images/image11.png",
            "doc/vpl/ui/svg/help/images/image12.png",
            "doc/vpl/ui/svg/help/images/image13.png",
            "doc/vpl/ui/svg/help/images/image14.png",
            "doc/vpl/ui/svg/help/images/image15.png",
            "doc/vpl/ui/svg/help/images/image16.png",
            "doc/vpl/ui/svg/help/images/image17.png",
            "doc/vpl/ui/svg/help/images/image18.png",
            "doc/vpl/ui/svg/help/images/image19.png",
            "doc/vpl/ui/svg/help/images/image1.png",
            "doc/vpl/ui/svg/help/images/image20.png",
            "doc/vpl/ui/svg/help/images/image21.png",
            "doc/vpl/ui/svg/help/images/image22.png",
            "doc/vpl/ui/svg/help/images/image23.png",
            "doc/vpl/ui/svg/help/images/image24.png",
            "doc/vpl/ui/svg/help/images/image25.png",
            "doc/vpl/ui/svg/help/images/image26.png",
            "doc/vpl/ui/svg/help/images/image27.png",
            "doc/vpl/ui/svg/help/images/image28.png",
            "doc/vpl/ui/svg/help/images/image29.png",
            "doc/vpl/ui/svg/help/images/image2.png",
            "doc/vpl/ui/svg/help/images/image30.png",
            "doc/vpl/ui/svg/help/images/image31.png",
            "doc/vpl/ui/svg/help/images/image32.png",
            "doc/vpl/ui/svg/help/images/image33.png",
            "doc/vpl/ui/svg/help/images/image34.png",
            "doc/vpl/ui/svg/help/images/image35.png",
            "doc/vpl/ui/svg/help/images/image36.png",
            "doc/vpl/ui/svg/help/images/image37.png",
            "doc/vpl/ui/svg/help/images/image38.png",
            "doc/vpl/ui/svg/help/images/image39.png",
            "doc/vpl/ui/svg/help/images/image3.png",
            "doc/vpl/ui/svg/help/images/image40.png",
            "doc/vpl/ui/svg/help/images/image41.png",
            "doc/vpl/ui/svg/help/images/image42.png",
            "doc/vpl/ui/svg/help/images/image43.png",
            "doc/vpl/ui/svg/help/images/image44.png",
            "doc/vpl/ui/svg/help/images/image45.png",
            "doc/vpl/ui/svg/help/images/image46.png",
            "doc/vpl/ui/svg/help/images/image47.png",
            "doc/vpl/ui/svg/help/images/image48.png",
            "doc/vpl/ui/svg/help/images/image49.png",
            "doc/vpl/ui/svg/help/images/image4.png",
            "doc/vpl/ui/svg/help/images/image50.png",
            "doc/vpl/ui/svg/help/images/image51.png",
            "doc/vpl/ui/svg/help/images/image52.png",
            "doc/vpl/ui/svg/help/images/image5.png",
            "doc/vpl/ui/svg/help/images/image6.png",
            "doc/vpl/ui/svg/help/images/image7.png",
            "doc/vpl/ui/svg/help/images/image8.png",
            "doc/vpl/ui/svg/help/images/image9.png",
        ]),
]
OPTIONS = {
    "packages": "sqlite3,tkinter,websocket,websockets",
    "dist_dir": ".",
    "plist": {
        "CFBundleIdentifier": "ch.epfl.mobots.vpl3server",
        "CFBundleVersion": "0.1",
        "NSHumanReadableCopyright":
            "2019-2020, École polytechnique fédérale de Lausanne (EPFL)",
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
