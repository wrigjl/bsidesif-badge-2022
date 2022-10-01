#!/bin/bash

echo "Starting copy"
ampy --port /dev/tty.usbserial-10 put funcs.py
ampy --port /dev/tty.usbserial-10 put api.py
ampy --port /dev/tty.usbserial-10 put pixel.py
#ampy --port /dev/tty.usbserial-10 put tokens.json  # Uncomment first time you push, then re-comment
# alternatively you can hand-run that command once
ampy --port /dev/tty.usbserial-10 put main.py
ampy --port /dev/tty.usbserial-10 put spectre.py
ampy --port /dev/tty.usbserial-10 put secrets.py
echo "Now copying primitives... may take a while"
ampy --port /dev/tty.usbserial-10 put primitives
