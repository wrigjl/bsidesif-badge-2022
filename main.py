import uasyncio as asyncio
from time import sleep as bad_juju
import funcs as fu
import pixel
import api
import gc

#import test

# Need to reduce memory footprint to start using buttons...
# Total bytes of memory to work with: 36,656
# Byte values aren't exact, they're plus or minus 500 bytes or so
# Bytes free after network / LED module 20,656 (16kb used)
# -- Now 21,872 after some changes
# Bytes free after using pushbutton library (test.py uses this): 12,256 (24,400kb used)
# -- Now ~13,720 after changes
# 16kb + 24.4kb > 36kb...
# -- Depending on some variables or changing factors... this COULD barely fit except
# the import itself overflows the memory
# Bummer because pushbutton library was nice
# Either reduce network module to < 12kb, reduce pushbutton library to < 20kb
# or build new pushbutton library which uses less than 20kb
# Will still need some overhead for communication between modules (e.g. badge modes)
# In summary...
# LIBRARY TOO CHONKY... detecting if a button is pressed is larger than the entire network module????
# time to re-implement unless memory footprint of library (or my code, or both!) can be reduced by ~5kb
# Might have to forgo short, double and long presses, and only have a basic short/long implementation

async def start_loop(coms: api.Coms, badge: pixel.Badge):
    event_colors = None
    while True:
        colors = tuple(badge.get_random_colors(event_colors=event_colors))
        badge.set_pixels(*colors)
        leds = badge.colors_to_rgb(*colors)
        response = coms.update_led_state(*leds, badge_write=True, web_write=True)
        if not response["event_active"]:
            badge.write_pixels()
            event_colors = response["leds"] if response["event_active"] else None
        await asyncio.sleep_ms(5000)


async def start_main():
    if 'wlan' not in locals():
        print(f'wlan did not exist')
        wlan = fu.conn()
    # while wlan.isconnected() == False:
    #     print(f'wlan is not connected')
    #     bad_juju(1)
    #     wlan = fu.reconn(wlan)
    #     print(f'After reconnect wlan is:{wlan.isconnected()}')
    uid = fu.get_uuid(wlan)
    print("My UUID: {}".format(uid))
    badge = pixel.Badge()
    coms = api.Coms(uid, badge)
    coms.badge_init()

    #asyncio.create_task(test.btn1()) # see comment at top of file
    asyncio.create_task(start_loop(coms, badge))

    while True:
        await asyncio.sleep_ms(5000)
        gc.collect()
        mem = gc.mem_free()
        print(f"{mem} bytes free")  # Print required so watchdog doesn't time out, so lets print memory free


if __name__ == '__main__':
    asyncio.run(start_main())
