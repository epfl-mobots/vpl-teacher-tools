# Author: Yves Piguet, EPFL
# Please don't redistribute without author's permission.

# utility functions related to local IP address and browser launch


class URLUtil:

    @staticmethod
    def get_local_IP():
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            try:
                s.connect(("128.178.255.255", 9))
                return s.getsockname()[0]
            except OSError:
                return "127.0.0.1"

    @staticmethod
    def teacher_tools_URL(port=None, path=None):
        ip = URLUtil.get_local_IP()
        return f"http://{ip}{':' + str(port) if port is not None else ''}{path or ''}"

    @staticmethod
    def start_browser(port=None, path=None, using=None):
        import webbrowser
        url = URLUtil.teacher_tools_URL(port, path)
        if using is not None:
            for browser in using:
                try:
                    webbrowser.get(browser).open(url, new=2)
                    return browser
                except Exception:
                    pass
        webbrowser.open(url, new=2)
