#!/bin/bash

esptool.py --port /dev/ttyUSB0 chip_id
esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0  ./firmware/esp8266-20220618-v1.19.1.bin
