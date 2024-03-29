#!/bin/bash
echo "
*************************************************************
***                                                       ***
***  To flash the board, you will need to rest the board  ***
***  into bootmode 3 times. to do this unplug the board   ***
***  and while holding the button, plug the board back in ***
***  You will be prompted when to do that.                 ***
***                                                       ***
***  if you have a USB hub that has a switch on it, that  ***
***  may be helful here.                                 ***
***                                                       ***
*************************************************************"

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
