VPL3Server.app is a self-contained server for VPL3 and the teacher tools. It creates a single data file with all the pupils and program data, "vpl.sqlite", located in your home directory (command-shift-H in the Finder).

For security reasons, macOS is more and more restrictive with which applications it accepts to run. This is usually a good thing. As a development version, VPL3Server.app is not signed. If you trust it (if you trust its provenance and if it was served encrypted over https), you can proceed as follows. In order to open it, at least the first time after you've downloaded it, should it fail, try this:

- right-click (or control-click) VPL3Server.app's icon to display a contextual menu
- choose Open
- if you open it directly from the disk image, in the dialog box, select "Don't warn me when opening applications on this disk image"
- click Open
- if a dialog asks "Do you want the application VPL3Server.app to accept incoming network connections?", click Allow.

If you've done all these steps and it fails once, try a second time.

VPL3Server-cxf.app is a strict equivalent of VPL3Server.app, but created with another tool (cx_Freeze instead of py2app). If you have difficulties with VPL3Server.app, or if you have the time to also test it and tell us what works for you, please test it as above. You should not run both applications at the same time. Both use the same files and the same TCP ports.

YP/201028
