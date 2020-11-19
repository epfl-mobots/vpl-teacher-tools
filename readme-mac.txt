VPL3Server.app is a self-contained server for VPL3 and the teacher tools. It creates a single data file with all the pupils and program data, "vplserver-db.sqlite", located in your home directory (command-shift-H in the Finder).

To install VPL3Server.app:

- double-click the .dmg file to open the disk image
- drag the VPL3Server.app file from the disk image to a convenient location on your hard disk, e.g. in the Applications folder (command-shift-A in the Finder) or to the Desktop (command-shift-D if you can't find the icon easily or you've got too many open windows).

For security reasons, macOS is more and more restrictive with which applications it accepts to run. This is usually a good thing. As a development version, VPL3Server.app is not signed. If you trust it (if you trust its provenance and if it was served encrypted over https), you can proceed as follows. In order to open it, at least the first time after you've downloaded it, should it fail (error message "VPL3Server.app cannot be opened because the developer cannot be verified" or equivalent), try this:

- click the Cancel button to discard the warning
- open the System Preferences
- click the Security & Privacy icon, tab "General"
- depending on the version of macOS, either allow to run applications which don't come from App Store and identified developers, or click the "Open Anyway" button next to the message about blocking VPL3Server.app.

Then try again to launch VPL3Server.app.

There is an alternative, more direct way to start unsigned applications:

- right-click (or control-click) VPL3Server.app's icon to display a contextual menu
- choose Open
- if you open it directly from the disk image, in the dialog box, select "Don't warn me when opening applications on this disk image"
- click Open
- if a dialog asks "Do you want the application VPL3Server.app to accept incoming network connections?", click Allow.

If you've done all these steps and it fails once, try a second time.

YP/201119
