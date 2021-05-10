import vpl3tt.com_http
import vpl3tt.com_ws
import vpl3tt.db
import vpl3tt.server_http
import vpl3tt.server_ws
import vpl3tt.server
import vpl3tt.urltiny
import vpl3tt.urlutil

def main():

    import sys
    args = sys.argv[1:]

    # find and remove "--ui UI" where UI is "tk", "wx", "osx", or "none"
    # (default: tk)
    ui = "tk"
    try:
        index = args.index("--ui")
        if index + 1 < len(args):
            ui = args[index + 1]
            del args[index : index + 2]
    except ValueError:
        pass

    from vpl3tt.launch import launch
    if ui == "tk":
        from vpl3tt.tkapp import Application
    elif ui == "wx":
        from vpl3tt.wxapp import Application
    elif ui == "osx":
        from vpl3tt.objcapp import Application
    elif ui == "none":
        from vpl3tt.noguiapp import Application
    else:
        print("Unsupported --ui option (should be tk (default), wx, osx or none)")
        sys.exit(1)

    launch(Application, args=args)
