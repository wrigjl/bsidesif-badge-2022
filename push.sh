#!/bin/bash

DEVICE=$1

echo "Starting copy"
ampy --port $DEVICE put funcs.py
ampy --port $DEVICE put api.py
ampy --port $DEVICE put pixel.py
ampy --port $DEVICE put tokens.json  # Comment after first push or you'll overwrite your token
# alternatively you can hand-run that command once and leave commented
ampy --port $DEVICE put main.py
ampy --port $DEVICE put spectre.py
ampy --port $DEVICE put secrets.py

