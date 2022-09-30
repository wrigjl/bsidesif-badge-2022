import time

import neopixel
import network
import urandom
from machine import Pin

import secrets

button_pin = Pin(0)
bit_depth = 5
num_neo_pixels = 3
np = neopixel.NeoPixel(Pin(4), num_neo_pixels)
pix_colors = {
    'red': (65, 0, 0), 'green': (0, 65, 0), 'blue': (0, 0, 65), 'yellow': (45, 55, 0),
    'purple': (65, 0, 65), 'magenta': (25, 0, 20), 'teal': (0, 25, 12), 'orange': (25, 10, 0)
}
display_colors = {
    'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255), 'yellow': (245, 255, 0),
    'purple': (255, 0, 255), 'orange': (250, 225, 0), 'magenta': (255, 0, 20), 'teal': (0, 250, 120)
}
color_array = [c for c in pix_colors]


def clear_pix(np, numpix):
    for i in range(numpix):
        np[i] = (0, 0, 0)
    np.write()


def set_pix(np, pix_0, pix_1, pix_2):
    pix_0 = str(pix_0).lower()
    pix_1 = str(pix_1).lower()
    pix_2 = str(pix_2).lower()
    for each in [pix_0, pix_1, pix_2]:
        if each not in pix_colors:
            return 42
    np[0] = pix_colors[pix_0]
    np[1] = pix_colors[pix_1]
    np[2] = pix_colors[pix_2]
    np.write()


def pixel(np, parr1, parr2, parr3):
    np[0] = parr1
    np[1] = parr2
    np[2] = parr3
    np.write()


def npix_random(np, event_colors=None):
    c1 = color_array[urandom.getrandbits(3)] if not event_colors else event_colors[0]["name"]
    c2 = color_array[urandom.getrandbits(3)] if not event_colors else event_colors[1]["name"]
    c3 = color_array[urandom.getrandbits(3)] if not event_colors else event_colors[2]["name"]
    np[0] = pix_colors[c1]
    np[1] = pix_colors[c2]
    np[2] = pix_colors[c3]
    np.write()
    return [
        # Convert tuples into lists
        [c for c in display_colors[c1]],
        [c for c in display_colors[c2]],
        [c for c in display_colors[c3]]
    ]


def fourpix_ran(np):
    pix_a = int(urandom.getrandbits(5))
    pix_b = int(urandom.getrandbits(5))
    pix_c = int(urandom.getrandbits(5))
    np[0] = (pix_a, pix_b, pix_c, pix_a)
    np[1] = (pix_c, pix_b, pix_a, pix_b)
    np[2] = (pix_c, pix_a, pix_b, pix_c)
    np.write()


def conn():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    # print(wlan.isconnected())
    return wlan


# Cycle a pin several times to identify if it works properly...
def test_pin(num):
    pin_num = Pin(num, Pin.OUT)
    for each in range(10):
        pin_num.off()
        time.sleep(.25)
        pin_num.on()
        time.sleep(.25)


if __name__ == "__main__":
    print('This is not supposed to run as a main module...')
