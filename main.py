import uasyncio as asyncio

import funcs as fu
import pixel
import api
import gc

#import test

# Need to reduce memory footprint to start using buttons...
# Total bytes of memory to work with: 36,656
# Bytes free after network / LED module 20,656 (16kb used)
# Bytes free after using pushbutton library (test.py uses this): 12,256 (24,400kb used)
# 16kb + 24.4kb > 36kb...
# Bummer because pushbutton library was nice
# Either reduce network module to < 12kb, reduce pushbutton library to < 20kb
# or build new pushbutton library which uses less than 20kb
# Will still need some overhead for communication between modules (e.g. badge modes)
# In summary...
# LIBRARY TOO CHONKY... detecting if a button is pressed is larger than the entire network module????
# time to re-implement unless memory footprint of library (or my code, or both!) can be reduced by ~5kb
# Might have to forgo short, double and long presses, and only have a basic short/long implementation

polling_time = 5
polling_clock = polling_time * 1000


def test_wireless(wlan, counter=0):
    if 'wlan' not in locals():
        print(f'wlan did not exist')
        wlan = fu.conn()
    if wlan.isconnected() == False:
        print('wlan is not connected {}'.format("" if counter == 0 else counter))
        wlan.connect()
    return wlan


async def start_loop(coms: api.Coms, badge: pixel.Badge):
    event_colors = None
    while True:
        colors = badge.get_random_colors(event_colors=event_colors)
        badge.set_pixels(*colors)
        leds = badge.colors_to_rgb(*colors)
        response = coms.update_led_state(*leds, badge_write=True, web_write=True)
        if not response["event_active"]:
            badge.write_pixels()
            event_colors = response["leds"] if response["event_active"] else None
        #time.sleep_ms(polling_clock)
        await asyncio.sleep_ms(polling_clock)


async def start_main():
    wlan = fu.conn()
    uid = fu.get_uuid()
    print("My UUID: {}".format(uid))
    badge = pixel.Badge(fu.np)
    coms = api.Coms(uid, badge)
    coms.badge_init()
    coms.add_prediction_state("255,128,255", "255,128,255", "255,128,255")
    #asyncio.create_task(test.btn1())
    asyncio.create_task(start_loop(coms, badge))

    # For some reason uncommenting this and the corresponding import
    # causes a crash
    # if I run test.py directly, it functions just fine.
    # ????
    while True:
        await asyncio.sleep_ms(5000)
        gc.collect()
        mem = gc.mem_free()
        print(f"{mem} bytes free")  # Print required so watchdog doesn't time out, so lets print memory free


if __name__ == '__main__':
    asyncio.run(start_main())
