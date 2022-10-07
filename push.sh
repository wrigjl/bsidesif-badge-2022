#!/bin/bash

DEVICE='/dev/ttyUSB0'
Json='false'
DFLAG='false'

while getopts 'jf:' flag
do
    case "${flag}" in
        f)
        DEVICE=$OPTARG
        DFLAG='true'
        ;;
        j) Json='true' ;;
        ?)
        echo "Bad arguments supplied"
        echo "Run as push.sh <-j>  -f [DEVICE_HANDLE]"
        exit 1
        ;;
    esac
done
shift "$(($OPTIND -1))"

if [ "$Json" = true ]
  then
    echo "Pushing tokens.json to $DEVICE"
    ampy --port $DEVICE put tokens.json
  else
    echo "skipped tokens.json"
fi

if [ "$DFLAG" = false ]
  then
    echo "No device supplied"
    echo "Running with default device handle of $DEVICE"
fi

echo "Starting copy to $DEVICE"
ampy --port $DEVICE put funcs.py
ampy --port $DEVICE put api.py
ampy --port $DEVICE put pixel.py
ampy --port $DEVICE put blinkers.py
# ampy --port $DEVICE put tokens.json  # Uncomment first time you push, then re-comment
# alternatively you can hand-run that command once
ampy --port $DEVICE put main.py
ampy --port $DEVICE put spectre.py
ampy --port $DEVICE put secrets.py
# echo "Now copying primitives... may take a while"
# ampy --port $DEVICE put primitives
