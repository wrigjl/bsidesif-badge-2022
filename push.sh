#!/bin/bash

DEVICE=$1

echo "Starting copy"
ampy --port $DEVICE put funcs.py
ampy --port $DEVICE put api.py
ampy --port $DEVICE put pixel.py
ampy --port $DEVICE put tokens.json  # Uncomment first time you push, then re-comment
# alternatively you can hand-run that command once
ampy --port $DEVICE put main.py
ampy --port $DEVICE put spectre.py
ampy --port $DEVICE put secrets.py
