# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# build distribution

DIR = vpl-teacher-distrib

ROOTFILES = \
	Makefile \
	launch.py \
	setup.py

PKGFILES = \
	vpl3/__init__.py \
	vpl3/cacaoapp.py \
	vpl3/com_http.py \
	vpl3/com_ws.py \
	vpl3/db.py \
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
	doc/index.html

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
	doc/vpl/ui/classic/classic.css \
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
	data/basic.json

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

VPL3Server.app: setup.py launch.py $(PKGFILES) $(DOCFILES) $(VPLFILES) $(THYMIOFILES) $(UICLASSICFILES) $(TOOLSFILES) $(QRFILES) $(DATAFILES)
	rm -rf build
	python3 setup.py py2app

VPLServer.dmg: VPL3Server.app
	rm -Rf "VPL Server" $@
	mkdir "VPL Server"
	cp -R $^ "VPL Server"
	hdiutil create -srcfolder "VPL Server" $@
	rm -Rf "VPL Server"

.PHONY: oh
oh:
	ohcount $(PKGFILES) launch.py setup.py $(DOCFILES) $(TOOLSFILES)
