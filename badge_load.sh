#!/bin/bash
echo "
*************************************************************
***                                                       ***
***  To flash the board, you will need to rest the board  ***
<<<<<<< HEAD
***  into bootmode then reset. just unplug the board and  ***
***  then while holding the button, plug the board back in ***
=======
***  into bootmode 3 times. to do this unplug the board   ***
***  and while holding the button, plug the board back in ***
>>>>>>> main
***  You will be prompted when to do that.                 ***
***                                                       ***
***  if you have a USB hub that has a switch on it, that  ***
***  may be helful here.                                 ***
***                                                       ***
*************************************************************"

<<<<<<< HEAD
=======
DEVICE=$1

echo "******** CHIP ID **********"
read -n 1 -s -r -p "Please reset board now, after press any key to continue"
esptool.py --port $DEVICE chip_id
echo "******** Erase Flash **********"
read -n 1 -s -r -p "Please reset board now, after press any key to continue"
esptool.py --port $DEVICE erase_flash
echo "******** FLASH CHIP **********"
read -n 1 -s -r -p "Please reset board now, after press any key to continue"
esptool.py --port $DEVICE --baud 460800 write_flash --flash_size=detect 0  ./firmware/esp8266-20220117-v1.18.bin
#!/bin/bash

>>>>>>> main
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

<<<<<<< HEAD
if [ "$DFLAG" = false ]
  then
    echo "No device supplied"
    echo "Running with default device handle of $DEVICE"
fi

echo "******** CHIP ID **********"
read -n 1 -s -r -p "Please reset board now, after press any key to continue"
esptool.py --port $DEVICE chip_id
echo "******** Erasing Flash **********"
# read -n 1 -s -r -p "Please reset board now, after press any key to continue"
esptool.py --port $DEVICE erase_flash
echo "******** FLASHING CHIP **********"
# read -n 1 -s -r -p "Please reset board now, after press any key to continue"
esptool.py --port $DEVICE --baud 460800 write_flash --flash_size=detect 0  ./firmware/esp8266-20220117-v1.18.bin

read -n 1 -s -r -p "Please reset board again now, after press any key to continue"

=======
>>>>>>> main
if [ "$Json" = true ]
  then
    echo "Pushing tokens.json to $DEVICE"
    ampy --port $DEVICE put tokens.json
  else
    echo "skipped tokens.json"
fi

<<<<<<< HEAD
=======
if [ "$DFLAG" = false ]
  then
    echo "No device supplied"
    echo "Running with default device handle of $DEVICE"
fi

>>>>>>> main
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
<<<<<<< HEAD
ampy --port $DEVICE run main.py

=======
>>>>>>> main
