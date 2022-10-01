import uasyncio as asyncio
import time

import api
import funcs as fu
import pixel
from primitives.pushbutton import Pushbutton

polling_time = 5
polling_clock = polling_time * 1000
long_press = 2
long_clock = long_press * 1000
debounce = 20


def test_wireless(wlan, counter=0):
    if 'wlan' not in locals():
        print(f'wlan did not exist')
        wlan = fu.conn()
    if wlan.isconnected() == False:
        print('wlan is not connected {}'.format("" if counter == 0 else counter))
        wlan.connect()
    return wlan


def double_click():
    print("double click detected")


def long_click():
    print("Long click detected")


def normal_click():
    print("Normal click detected")


async def button_handler():
    button = fu.button_pin
    pb = Pushbutton(button, suppress=True)
    # pb.double_func(double_click, ())
    # pb.long_func(long_click, ())
    pb.press_func(normal_click, ())
    while True:
        yield 1


async def start_led_handler():
    wlan = fu.conn()
    uid = fu.get_uuid()
    print("My UUID: {}".format(uid))
    badge = pixel.Badge(fu.np)
    coms = api.Coms(uid, badge)
    coms.add_prediction_state("255,128,255", "255,128,255", "255,128,255")
    start_time = time.ticks_ms()
    event_colors = None
    while True:
        colors = badge.get_random_colors(event_colors=event_colors)
        badge.set_pixels(*colors)
        leds = badge.colors_to_rgb(*colors)
        response = coms.update_led_state(*leds, badge_write=True)
        if not response["event_active"]:
            badge.write_pixels()
            event_colors = response["leds"] if response["event_active"] else None
        await asyncio.sleep_ms(polling_clock)
        yield 1


if __name__ == '__main__':
    asyncio.run(button_handler())
    asyncio.run(start_led_handler())
