# Setup file to create Windows or Mac app using cx_Freeze
# To run it:
# - Windows: in PowerShell, type
#   python3 setup_cx_freeze.py bdist_msi
# The result is a .msi file in directory dist
# - Mac: in Terminal, for just the .app application, type
#   python3 setup_cx_freeze.py bdist_mac
# or for the application in a dmg disk image:
#   python3 setup_cx_freeze.py bdist_dmg

import sys, os
from cx_Freeze import setup, Executable

__version__ = "0.1.0"

include_files = []
excludes = [
	"curses",
	"lib2to3",
	"numpy",
	"xmlrpc",
]
packages = ["os", "json",]

build_exe = {
    "packages": packages,
    "include_files": include_files,
    "excludes": excludes,
}
launcher = "launch_tk.py"
base = None
options = {
    "build_exe": build_exe,
}
setup_options = {
    "name": "VPL3Server-cx-Freeze",
    "description": "VPL3 Teacher Tools built with cx_Freeze",
    "version": __version__,
    "options": options,
}

if sys.platform == "win32":
    base = "Win32GUI"
    build_exe["include_msvcr"] = False
    # the end-user should download and install
    # https://aka.ms/vs/16/release/vc_redist.x64.exe
elif sys.platform == "darwin":
    launcher = "launch_objc.py"
    setup_options["bundle_name"] = "VPL3 Server"

setup(
    **setup_options,
    executables=[Executable(launcher, base=base)],
)
