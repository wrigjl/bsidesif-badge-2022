<<<<<<< HEAD
import secrets

import uasyncio as asyncio
import network
import blinkers
=======
import uasyncio as asyncio
from time import sleep as bad_juju
>>>>>>> main
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

<<<<<<< HEAD
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
=======
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
>>>>>>> main
    event_colors = None
    while True:
        colors = tuple(badge.get_random_colors(event_colors=event_colors))
        badge.set_pixels(*colors)
        leds = badge.colors_to_rgb(*colors)
        response = coms.update_led_state(*leds, badge_write=True, web_write=True)
        if not response["event_active"]:
            badge.write_pixels()
            event_colors = response["leds"] if response["event_active"] else None
        await asyncio.sleep_ms(30000)


def click(coms):
    print("Click button sequence!")
    response = coms.press()
    if "success" in response and response["success"]:
        if "message" in response and "no events active" in response["message"]:
            prestates = (coms.badge.c1, coms.badge.c2, coms.badge.c3)
            asyncio.create_task(blinkers.blink_off(coms.badge, c1=prestates[0], c2=prestates[1], c3=prestates[2]))


async def btn_listener(coms: api.Coms):
    button = Pin(0)
    pb = Pushbutton(button, suppress=True)
    pb.release_func(click, (coms,))
    await asyncio.sleep_ms(1000)


async def start_network_testing(wlan):
    while True:
        if not wlan.active():
            wlan.active(True)
            wlan.connect(secrets.SSID, secrets.PASSWORD)
            connect_attempts = 0
            while not wlan.isconnected():
                await asyncio.sleep_ms(1000)
                connect_attempts += 1
            print("Wifi connected!")
        if wlan.active():
            if not wlan.isconnected():
                print("Wifi disconnect, attempting re-connect")
                wlan.connect(secrets.SSID, secrets.PASSWORD)
            else:
                print("Wifi still active!")
        await asyncio.sleep_ms(5000)
        print(".")  # Need to figure out wdt.feed()
        await asyncio.sleep_ms(5000)
        print(".")


async def start_main():
<<<<<<< HEAD
    uid = fu.get_uuid()
=======
    if 'wlan' not in locals():
        print(f'wlan did not exist')
        wlan = fu.conn()
    # while wlan.isconnected() == False:
    #     print(f'wlan is not connected')
    #     bad_juju(1)
    #     wlan = fu.reconn(wlan)
    #     print(f'After reconnect wlan is:{wlan.isconnected()}')
    uid = fu.get_uuid(wlan)
>>>>>>> main
    print("My UUID: {}".format(uid))
    badge = pixel.Badge()
    coms = api.Coms(uid, badge, badge_server="http://game.ifhacker.org")
    try:
        wlan = network.WLAN(network.STA_IF)
        asyncio.create_task(start_network_testing(wlan))
    except Exception as e:
        print(e)
        asyncio.run(blinkers.blink(badge, cycles=5, c1="off", c3="off", msg="Error initiating wifi"))
        return
    sim = False  # Set to True to simulate connection error
    sim_counter = 3
    while not coms.badge_init(simulate_failure=sim):
        asyncio.run(blinkers.blink(badge))
        sim_counter -= 1
        if sim_counter <= 0:
            sim = False

    badge.set_lock_updates()

    blue = (0, 0, 25)
    badge.secret_write(blue, blue, blue)

    asyncio.create_task(start_com_loop(coms, badge))
    asyncio.create_task(btn_listener(coms))
    asyncio.run(blinkers.half_blink(badge, cycles=3, c1="green", c2="green", c3="green", msg="Task init success"))
    badge.secret_write(blue, blue, blue)
    badge.set_lock_updates(lock=False)

    while True:
        await asyncio.sleep_ms(5000)
        gc.collect()
        mem = gc.mem_free()
        print(f"{mem} bytes free")  # Print required so watchdog doesn't time out, so lets print memory free


if __name__ == '__main__':
    while True:
        asyncio.run(start_main())
        print("Restarting main thread...")
