# Setup file to create Windows app using cs_Freeze
# To run it: in PowerShell, type
#   python3 setup_exe.py bdist_msi
# The result is a .msi file in directory dist

import sys, os
from cx_Freeze import setup, Executable

__version__ = "0.1.0"

include_files = []
excludes = []
packages = ["os", "json",]

setup(
		name="vpl3tt",
		description="VPL3 Teacher Tools",
		version=__version__,
		options={
			"build_exe": {
				"packages": packages,
				"include_files": include_files,
				"excludes": excludes,
				"include_msvcr": True,
			},
		},
		executables=[Executable("launch_tk.py", base="Win32GUI")],
)

