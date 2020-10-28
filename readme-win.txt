VPL3Server is a self-contained server for VPL3 and the teacher tools. It creates
a single data file with all the pupils and program data, "vpl.sqlite", located
in your home directory (typically C:\Users\username; you can use %USERPROFILE%
in a shell or directly in the address bar of the File Explorer).

For security reasons, Windows is more and more restrictive with which
applications it accepts to run. This is usually a good thing. As a development
version, VPL3Server is not signed. If you trust it (if you trust its provenance
and if it was served encrypted over https), you can accept all questions.

To install:

- Unless you're sure to already have done it or you've installed Visual Studio,
download https://aka.ms/vs/16/release/vc_redist.x64.exe and double-click it to
install Microsoft libraries required by VPL3Server.

- Double-click the .msi file and proceed until the end.

A shortcut named "VPL3 Server" will be created on the Desktop.

To uninstall, open the .msi file again; you'll be asked whether you want to
repair it or remove it.

YP/201028
