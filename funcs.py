import network
import ubinascii
from machine import Pin

import secrets

button_pin = Pin(0)

# Updating neopixel values has been moved to pixel.py


def get_uuid(wlan_sta):
    wlan_mac = wlan_sta.config('mac')
    mac = ubinascii.hexlify(wlan_mac).decode()
    return "ebc626d8-6ddb-437c-8210-{}".format(mac)


def conn():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    return wlan

def reconn(wlan):
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    print(f'Wifi connection is: {wlan.isconnected()}')
    return wlan


# Cycle a pin several times to identify if it works properly...
# def test_pin(num):
#     pin_num = Pin(num, Pin.OUT)
#     for each in range(10):
#         pin_num.off()
#         time.sleep(.25)
#         pin_num.on()
#         time.sleep(.25)
