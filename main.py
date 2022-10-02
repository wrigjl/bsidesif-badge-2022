import uasyncio as asyncio

import funcs as fu
import pixel
import api
import gc
from machine import Pin


async def _g():
    pass
type_coro = type(_g())


def launch(func, tup_args):
    res = func(*tup_args)
    if isinstance(res, type_coro):
        res = asyncio.create_task(res)
    return res


class Pushbutton:
    debounce_ms = 50

    def __init__(self, pin, suppress=True):
        self._pin = pin  # Initialise for input
        self._supp = suppress
        self._dblpend = False  # Doubleclick waiting for 2nd click
        self._dblran = False  # Doubleclick executed user function
        self._tf = False
        self._ff = False
        self._df = False
        # Convert from electrical to logical value
        self._state = self.rawstate()  # Initial state
        self._run = asyncio.create_task(self._go())  # Thread runs forever

    async def _go(self):
        while True:
            self._check(self.rawstate())
            # Ignore state changes until switch has settled. Also avoid hogging CPU.
            # See https://github.com/peterhinch/micropython-async/issues/69
            await asyncio.sleep_ms(Pushbutton.debounce_ms)

    def _check(self, state):
        if state == self._state:
            return
        # State has changed: act on it now.
        self._state = state
        if state:  # Button pressed: launch pressed func
            if self._tf:
                launch(self._tf, self._ta)
        else:  # Button release. Is there a release func?
            if self._ff:
                launch(self._ff, self._fa)
            self._dblran = False

    # ****** API ******
    def press_func(self, func=False, args=()):
        if func is None:
            self.press = asyncio.Event()
        self._tf = self.press.set if func is None else func
        self._ta = args

    def release_func(self, func=False, args=()):
        if func is None:
            self.release = asyncio.Event()
        self._ff = self.release.set if func is None else func
        self._fa = args

    # Current non-debounced logical button state: True == pressed
    def rawstate(self):
        p1 = self._pin()
        p2 = self._pin.value()
        active = p1 == 1 and p2 == 1
        return active

    # Current debounced state of button (True == pressed)
    def __call__(self):
        return self._state

    def deinit(self):
        self._run.cancel()


async def start_com_loop(coms: api.Coms, badge: pixel.Badge):
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


def click(coms):
    print("Click button sequence!")
    coms.press()


async def btn_listener(coms: api.Coms):
    button = Pin(0)
    pb = Pushbutton(button, suppress=True)
    pb.release_func(click, (coms,))
    await asyncio.sleep_ms(1000)


async def start_main():
    wlan = fu.conn()
    uid = fu.get_uuid()
    print("My UUID: {}".format(uid))
    badge = pixel.Badge()
    coms = api.Coms(uid, badge, badge_server="http://game.ifhacker.org")
    coms.badge_init()

    asyncio.create_task(start_com_loop(coms, badge))
    asyncio.create_task(btn_listener(coms))

    while True:
        await asyncio.sleep_ms(5000)
        gc.collect()
        mem = gc.mem_free()
        print(f"{mem} bytes free")  # Print required so watchdog doesn't time out, so lets print memory free


if __name__ == '__main__':
    asyncio.run(start_main())
