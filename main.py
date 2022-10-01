from uasyncio import create_task, sleep_ms, run
import funcs as fu
import api
import gc

#import test


async def start_com_loop(coms: api.Coms):
    event_colors = None
    while True:
        colors = tuple(coms.get_random_colors(event_colors=event_colors))
        coms.set_pixels(*colors)
        leds = coms.colors_to_rgb(*colors)
        response = coms.update_led_state(*leds, badge_write=True, web_write=True)
        if not response["event_active"]:
            coms.write_pixels()
            event_colors = response["leds"] if response["event_active"] else None
        await sleep_ms(5000)


async def start_main():
    wlan = fu.conn()
    uid = fu.get_uuid()
    print("My UUID: {}".format(uid))
    coms = api.Coms(uid)
    coms.badge_init()

    #asyncio.create_task(test.btn1()) # see comment at top of file
    create_task(start_com_loop(coms))
    # asyncio.create_task(button_sensor(coms))

    while True:
        await sleep_ms(3000)
        gc.collect()
        mem = gc.mem_free()
        print(f"{mem} bytes free")  # Print required so watchdog doesn't time out, so lets print memory free


if __name__ == '__main__':
    run(start_main())
