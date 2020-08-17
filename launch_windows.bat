@echo off
set p=python
set pw=pythonw
where /q "%p%"
if errorlevel 1 (
	set p=python3
	set pw=pythonw3
	where /q "%p%"
	if errorlevel 1 (
		set p="%userprofile%\AppData\Local\Programs\Python\Launcher\py.exe"
		set pw="%userprofile%\AppData\Local\Programs\Python\Launcher\pyw.exe"
		if not exist "%p%" (
			set p="%userprofile%\AppData\Local\Microsoft\WindowsApps\python3.exe"
			set pw="%userprofile%\AppData\Local\Microsoft\WindowsApps\pythonw3.exe"
			if not exist "%p" (
				set p=python
				set pw=pythonw
			)
		)
	)
)
"%p%" -m pip install websocket websockets qrcode
start "%pw%" launch_tk.py
exit
