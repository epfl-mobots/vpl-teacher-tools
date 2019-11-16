# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# build distribution

DIR = vpl-teacher-distrib

ROOTFILES = \
	Makefile \
	launch_objc.py \
	launch_tk.py \
	launch_wx.py \
	setup.py

PKGFILES = \
	vpl3/__init__.py \
	vpl3/cacaoapp.py \
	vpl3/com_http.py \
	vpl3/com_ws.py \
	vpl3/db.py \
	vpl3/launch.py \
	vpl3/server.py \
	vpl3/server_http.py \
	vpl3/server_ws.py \
	vpl3/tkapp.py \
	vpl3/urltiny.py \
	vpl3/urlutil.py \
	vpl3/wxapp.py

DOCFILES = \
	doc/client.js \
	doc/db.html \
	doc/index.html \
	doc/login.fr.html \
	doc/tt.html

VPLFILES = \
	doc/vpl/EPFL_Logo_SVG.svg \
	doc/vpl/grs_logo_RGB.svg \
	doc/vpl/Logo_vpl.svg \
	doc/vpl/vpl-about.html \
	doc/vpl/vpl.html \
	doc/vpl/vpl-min.js

THYMIOFILES = \
	doc/vpl/thymio/thymio.js

UICLASSICFILES = \
	doc/vpl/ui/classic/block-english.json \
	doc/vpl/ui/classic/block-french.json \
	doc/vpl/ui/classic/classic.css \
	doc/vpl/ui/classic/cmd-sim-english.json \
	doc/vpl/ui/classic/cmd-sim-french.json \
	doc/vpl/ui/classic/cmd-vpl-english.json \
	doc/vpl/ui/classic/cmd-vpl-french.json \
	doc/vpl/ui/classic/french.json \
	doc/vpl/ui/classic/ui.json

TOOLSFILES = \
	doc/vpl-teacher-tools/dashboard.html \
	doc/vpl-teacher-tools/dashboard.js \
	doc/vpl-teacher-tools/dev.html \
	doc/vpl-teacher-tools/doc.html \
	doc/vpl-teacher-tools/filebrowser.html \
	doc/vpl-teacher-tools/filebrowser.js \
	doc/vpl-teacher-tools/html-tools.css \
	doc/vpl-teacher-tools/initdb-dev.html \
	doc/vpl-teacher-tools/Logo_vpl.svg \
	doc/vpl-teacher-tools/ns.js \
	doc/vpl-teacher-tools/pairing.html \
	doc/vpl-teacher-tools/pairing.js \
	doc/vpl-teacher-tools/README.md \
	doc/vpl-teacher-tools/students.html \
	doc/vpl-teacher-tools/students.js \
	doc/vpl-teacher-tools/student-debug.html \
	doc/vpl-teacher-tools/student-debug.js \
	doc/vpl-teacher-tools/ui.json \
	doc/vpl-teacher-tools/util-url.js \
	doc/vpl-teacher-tools/vpl.html \
	doc/vpl-teacher-tools/vpl-about.html \
    doc/vpl-teacher-tools/vpl_load.png \
    doc/vpl-teacher-tools/vpl_new.png \
    doc/vpl-teacher-tools/vpl_run.png \
    doc/vpl-teacher-tools/vpl_stop.png

QRFILES = \
	doc/libs/qrcodejs/LICENSE \
	doc/libs/qrcodejs/README.md \
	doc/libs/qrcodejs/qrcode.min.js

DATAFILES = \
	data/basic-sensors.vpl3ui \
	data/basic-touch.vpl3ui \
	data/basic-track.vpl3ui \
	data/simple-sensors.vpl3ui \
	data/simple-touch.vpl3ui \
	data/simple-track.vpl3ui

.PHONY: all
all:
	rm -Rf $(DIR)
	mkdir -p $(DIR)/vpl3
	mkdir -p $(DIR)/doc/vpl/thymio
	mkdir -p $(DIR)/doc/vpl/ui/classic
	mkdir -p $(DIR)/doc/vpl-teacher-tools
	mkdir -p $(DIR)/doc/libs/qrcodejs
	mkdir -p $(DIR)/data
	cp -p $(ROOTFILES) $(DIR)
	cp -p $(PKGFILES) $(DIR)/vpl3
	cp -p $(DOCFILES) $(DIR)/doc
	cp -p $(VPLFILES) $(DIR)/doc/vpl
	cp -p $(THYMIOFILES) $(DIR)/doc/vpl/thymio
	cp -p $(UICLASSICFILES) $(DIR)/doc/vpl/ui/classic
	cp -p $(TOOLSFILES) $(DIR)/doc/vpl-teacher-tools
	cp -p $(QRFILES) $(DIR)/doc/libs/qrcodejs
	cp -p $(DATAFILES) $(DIR)/data
	zip -r - $(DIR) >$(DIR).zip

VPL3Server.app: setup.py launch_objc.py $(PKGFILES) $(DOCFILES) $(VPLFILES) $(THYMIOFILES) $(UICLASSICFILES) $(TOOLSFILES) $(QRFILES) $(DATAFILES)
	rm -rf build
	python3 setup.py py2app

.PHONY: VPL3Server.app
VPLServer.dmg: VPL3Server.app
	rm -Rf "VPL Server" $@
	mkdir "VPL Server"
	cp -R $^ "VPL Server"
	hdiutil create -srcfolder "VPL Server" $@
	rm -Rf "VPL Server"

ServeFile.dmg: Serve\ File.app
	rm -Rf "Serve File" $@
	mkdir "Serve File"
	cp -R "$^" "Serve File"
	hdiutil create -srcfolder "Serve File" $@
	rm -Rf "Serve File"

.PHONY: Serve\ File.app
Serve\ File.app: setup_serve_via_http.py serve_via_http.py
	rm -rf build
	python3 setup_serve_via_http.py py2app

.PHONY: oh
oh:
	ohcount $(PKGFILES) $(ROOTFILES) $(DOCFILES) $(TOOLSFILES)
