# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# build distribution

DIR = vpl-teacher-distrib

ROOTFILES = \
	Makefile \
	launch_objc.py \
	launch_tk.py \
	launch_windows.bat \
	launch_mac.command \
	launch_wx.py \
	setup.py

VPL3PKGFILES = \
	vpl3/__init__.py \
	vpl3/baseapp.py \
	vpl3/cacaoapp.py \
	vpl3/com_http.py \
	vpl3/com_ws.py \
	vpl3/db.py \
	vpl3/launch.py \
	vpl3/server.py \
	vpl3/server_http.py \
	vpl3/server_thymio.py \
	vpl3/server_ws.py \
	vpl3/tkapp.py \
	vpl3/translate.py \
	vpl3/translate_fr.py \
	vpl3/urltiny.py \
	vpl3/urlutil.py \
	vpl3/wxapp.py

THYMIOPKGFILES = \
	thymio/__init__.py \
	thymio/assembler.py \
	thymio/message.py \
	thymio/connection.py \
	thymio/thymio.py \

DOCFILES = \
	doc/client.js \
	doc/db.html \
	doc/index.html \
	doc/login.html \
	doc/login.fr.html \
	doc/login-gui.js \
	doc/tr-mappings.json \
	doc/tt.html \
	doc/tt.fr.html

VPLFILES = \
	doc/vpl/EPFL_Logo_SVG.svg \
	doc/vpl/grs_logo_RGB.svg \
	doc/vpl/Logo_vpl.svg \
	doc/vpl/vpl-about.html \
	doc/vpl/vpl.html \
	doc/vpl/vpl-min.js

THYMIOFILES = \
	doc/vpl/thymio/thymio.js

UIFILES = \
	doc/vpl/ui/toc.json

UICLASSICFILES = \
	doc/vpl/ui/classic/aesl.json \
	doc/vpl/ui/classic/aseba.json \
	doc/vpl/ui/classic/block-english.json \
	doc/vpl/ui/classic/block-french.json \
	doc/vpl/ui/classic/block-list.json \
	doc/vpl/ui/classic/classic.css \
	doc/vpl/ui/classic/cmd-sim-english.json \
	doc/vpl/ui/classic/cmd-sim-french.json \
	doc/vpl/ui/classic/cmd-vpl-english.json \
	doc/vpl/ui/classic/cmd-vpl-french.json \
	doc/vpl/ui/classic/doctemplate-english.html \
	doc/vpl/ui/classic/doctemplate-french.html \
	doc/vpl/ui/classic/french.json \
	doc/vpl/ui/classic/help-blocks-english.json \
	doc/vpl/ui/classic/help-blocks-french.json \
	doc/vpl/ui/classic/help-buttons-english.json \
	doc/vpl/ui/classic/help-buttons-french.json \
	doc/vpl/ui/classic/js.json \
	doc/vpl/ui/classic/l2.json \
	doc/vpl/ui/classic/python.json \
	doc/vpl/ui/classic/typical-param-set.json \
	doc/vpl/ui/classic/typical-states.json \
	doc/vpl/ui/classic/ui.json

UISVGFILES = \
	doc/vpl/ui/svg/aesl.json \
	doc/vpl/ui/svg/aseba.json \
	doc/vpl/ui/svg/block-english.json \
	doc/vpl/ui/svg/block-french.json \
	doc/vpl/ui/svg/block-list.json \
	doc/vpl/ui/svg/Blocks.svg \
	doc/vpl/ui/svg/Blocks16.svg \
	doc/vpl/ui/svg/buttons.json \
	doc/vpl/ui/svg/cmd-sim-english.json \
	doc/vpl/ui/svg/cmd-sim-french.json \
	doc/vpl/ui/svg/cmd-vpl-english.json \
	doc/vpl/ui/svg/cmd-vpl-french.json \
	doc/vpl/ui/svg/doctemplate-english.html \
	doc/vpl/ui/svg/doctemplate-french.html \
	doc/vpl/ui/svg/english.json \
	doc/vpl/ui/svg/french.json \
	doc/vpl/ui/svg/help-blocks-english.json \
	doc/vpl/ui/svg/help-blocks-french.json \
	doc/vpl/ui/svg/Icons.svg \
	doc/vpl/ui/svg/js.json \
	doc/vpl/ui/svg/l2.json \
	doc/vpl/ui/svg/python.json \
	doc/vpl/ui/svg/svg.css \
	doc/vpl/ui/svg/toolbars.json \
	doc/vpl/ui/svg/ui.json

TOOLSFILES = \
	doc/vpl-teacher-tools/dashboard-gui.js \
	doc/vpl-teacher-tools/dashboard.html \
	doc/vpl-teacher-tools/dashboard.fr.html \
	doc/vpl-teacher-tools/dashboard.js \
	doc/vpl-teacher-tools/dev.html \
	doc/vpl-teacher-tools/dev.fr.html \
	doc/vpl-teacher-tools/doc.html \
	doc/vpl-teacher-tools/doc.fr.html \
	doc/vpl-teacher-tools/filebrowser-gui.js \
	doc/vpl-teacher-tools/filebrowser.html \
	doc/vpl-teacher-tools/filebrowser.fr.html \
	doc/vpl-teacher-tools/filebrowser.js \
	doc/vpl-teacher-tools/filedialog.js \
	doc/vpl-teacher-tools/html-tools.css \
	doc/vpl-teacher-tools/icon-file-vpl3.svg \
	doc/vpl-teacher-tools/icon-file-vpl3ui.svg \
	doc/vpl-teacher-tools/initdb-dev-gui.js \
	doc/vpl-teacher-tools/initdb-dev.html \
	doc/vpl-teacher-tools/initdb-dev.fr.html \
	doc/vpl-teacher-tools/json-ws-bridge-api.js \
	doc/vpl-teacher-tools/login.js \
	doc/vpl-teacher-tools/Logo_vpl.svg \
	doc/vpl-teacher-tools/ns.js \
	doc/vpl-teacher-tools/pairing-gui.js \
	doc/vpl-teacher-tools/pairing.html \
	doc/vpl-teacher-tools/pairing.fr.html \
	doc/vpl-teacher-tools/robots.js \
	doc/vpl-teacher-tools/pairing.js \
	doc/vpl-teacher-tools/README.md \
	doc/vpl-teacher-tools/students.html \
	doc/vpl-teacher-tools/students-gui.js \
	doc/vpl-teacher-tools/students.js \
	doc/vpl-teacher-tools/students.fr.html \
	doc/vpl-teacher-tools/student-debug.html \
	doc/vpl-teacher-tools/student-debug.js \
	doc/vpl-teacher-tools/translate.js \
	doc/vpl-teacher-tools/ui.json \
	doc/vpl-teacher-tools/util-files.js \
	doc/vpl-teacher-tools/util-url.js \
	doc/vpl-teacher-tools/vpl-about.html \
	doc/vpl-teacher-tools/vpl-gui.js \
	doc/vpl-teacher-tools/vpl.html \
	doc/vpl-teacher-tools/vpl.fr.html \
	doc/vpl-teacher-tools/vplurl.js \
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
	mkdir -p $(DIR)/thymio
	mkdir -p $(DIR)/doc/vpl/thymio
	mkdir -p $(DIR)/doc/vpl/ui/classic
	mkdir -p $(DIR)/doc/vpl/ui/svg
	mkdir -p $(DIR)/doc/vpl-teacher-tools
	mkdir -p $(DIR)/doc/libs/qrcodejs
	mkdir -p $(DIR)/data
	cp -p $(ROOTFILES) $(DIR)
	cp -p $(VPL3PKGFILES) $(DIR)/vpl3
	cp -p $(THYMIOPKGFILES) $(DIR)/thymio
	cp -p $(DOCFILES) $(DIR)/doc
	cp -p $(VPLFILES) $(DIR)/doc/vpl
	cp -p $(THYMIOFILES) $(DIR)/doc/vpl/thymio
	cp -p $(UIFILES) $(DIR)/doc/vpl/ui
	cp -p $(UICLASSICFILES) $(DIR)/doc/vpl/ui/classic
	cp -p $(UISVGFILES) $(DIR)/doc/vpl/ui/svg
	cp -p $(TOOLSFILES) $(DIR)/doc/vpl-teacher-tools
	cp -p $(QRFILES) $(DIR)/doc/libs/qrcodejs
	cp -p $(DATAFILES) $(DIR)/data
	zip -r - $(DIR) >$(DIR).zip

.PHONY: VPL3Server.app
VPL3Server.app: setup.py launch_objc.py $(VPL3PKGFILES) $(THYMIOPKGFILES) $(DOCFILES) $(VPLFILES) $(THYMIOFILES) $(UIFILES) $(UICLASSICFILES) $(UISVGFILES) $(TOOLSFILES) $(QRFILES) $(DATAFILES)
	rm -rf build
	python3 setup.py py2app

VPLServer.dmg: VPL3Server.app readme-mac.txt
	rm -Rf "VPL Server" $@
	mkdir "VPL Server"
	cp -R $^ "VPL Server"
	hdiutil create -format UDZO -imagekey zlib-level=9 -srcfolder "VPL Server" $@
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
