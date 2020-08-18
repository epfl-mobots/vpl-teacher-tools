#!/bin/sh

# install the required packages and launch the server with the existing python3

cd `echo "$0" | sed -e 's/\/[^\/]*$//'`

python3 -m pip install websocket websockets qrcode
python3 launch_objc.py &

