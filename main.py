import secrets

import uasyncio as asyncio
import network
import blinkers
import funcs as fu
import pixel
import api
import gc
from machine import Pin, WDT


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
        self._pin = pin
        self._supp = suppress
        self._dblpend = False
        self._dblran = False
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
    time_between_updates = 30  # seconds
    ramp_up = 1
    while True:
        colors = tuple(badge.get_random_colors(event_colors=event_colors))
        badge.set_pixels(*colors)
        leds = badge.colors_to_rgb(*colors)
        response = coms.update_led_state(*leds, badge_write=True, web_write=True)
        if not response["event_active"]:
            badge.write_pixels()
            event_colors = response["leds"] if response["event_active"] else None
        for i in range(0, ramp_up):
            await asyncio.sleep_ms(1000)
        ramp_up += 5
        if ramp_up >= time_between_updates:
            ramp_up = time_between_updates
        fu.wdt.feed()


def click(coms):
    print("Click button sequence!")
    fu.wdt.feed()
    response = coms.press()
    fu.wdt.feed()
    if "success" in response and response["success"]:
        if "message" in response and "no events active" in response["message"]:
            prestates = (coms.badge.c1, coms.badge.c2, coms.badge.c3)
            asyncio.create_task(blinkers.blink_off(coms.badge, c1=prestates[0], c2=prestates[1], c3=prestates[2]))


async def btn_listener(coms: api.Coms):
    button = Pin(0)
    pb = Pushbutton(button, suppress=True)
    pb.release_func(click, (coms,))
    fu.wdt.feed()
    await asyncio.sleep_ms(1000)


async def start_network_testing(wlan):
    task_start = True
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
                if not task_start:
                    print("Wifi disconnect, attempting re-connect")
                wlan.connect(secrets.SSID, secrets.PASSWORD)
            else:
                if not task_start:
                    print("Wifi still active!")
        task_start = False
        for i in range(0, 15):
            await asyncio.sleep_ms(1000)
            fu.wdt.feed()


def failed_token_generation(badge):
    # If token registration fails, don't be a boring badge :)
    asyncio.run(blinkers.half_blink(
        badge,
        c1="teal", c2="magenta", c3="teal",
        cycles=10, msg="Offline state"
    ))
    fu.wdt.feed()
    asyncio.run(blinkers.run_pattern(badge, pattern_repeat=3))
    fu.wdt.feed()


def init_badge(coms, badge):
    sim = False  # Set to True to simulate connection error
    sim_counter = 6
    init_attempt = 0
    com_init_success = False
    while not com_init_success:
        fu.wdt.feed()
        com_init_success = coms.badge_init(simulate_failure=sim, init_attempt=init_attempt)
        if not com_init_success:
            asyncio.run(blinkers.blink(badge))
            sim_counter -= 1
            init_attempt += 1
            if sim_counter <= 0:
                sim = False
            if init_attempt > 5:
                return com_init_success
    return com_init_success


async def start_main():
    uid = fu.get_uuid()
    print("My UUID: {}".format(uid))
    badge = pixel.Badge()
    coms = api.Coms(uid, badge, badge_server="http://game.ifhacker.org")

    wlan = network.WLAN(network.STA_IF)
    asyncio.create_task(start_network_testing(wlan))
    print("Awaiting initial wifi connection")
    connect_attempts = 0
    badge.set_lock_updates()
    badge.secret_write(
        (0, 0, 0),
        (0, 52, 24),
        (0, 0, 0)
    )
    while not wlan.isconnected() or connect_attempts < 20:
        await asyncio.sleep_ms(500)
        if connect_attempts % 6 == 0:
            badge.secret_write(
                (60, 0, 0),
                (0, 52, 24),
                (60, 0, 0)
            )
            await asyncio.sleep_ms(700)
            badge.secret_write(
                (0, 0, 0),
                (0, 52, 24),
                (0, 0, 0)
            )
            fu.wdt.feed()
        connect_attempts += 1

    if wlan.isconnected():
        print("Wifi connected")
    else:
        print("Wifi failed to connect, falling back to offline state.")
    badge.set_lock_updates(lock=False)

    badge_initiated = False
    while not badge_initiated:
        print("Attempting badge init")
        badge_initiated = init_badge(coms, badge)
        if not badge_initiated:
            print("Badge init failed, running offline loop")
            failed_token_generation(badge)
            print("Re-attempting badge init")
    print("Badge init success")

    badge.set_lock_updates()

    blue = (0, 0, 25)
    badge.secret_write(blue, blue, blue)

    asyncio.create_task(start_com_loop(coms, badge))
    asyncio.create_task(btn_listener(coms))
    asyncio.run(blinkers.half_blink(badge, cycles=3, c1="green", c2="green", c3="green", msg="Task init success"))
    badge.secret_write(blue, blue, blue)
    badge.set_lock_updates(lock=False)

    gc.collect()
    mem = gc.mem_free()
    print(f"{mem} bytes free")

    while True:
        for i in range(0, 15):
            await asyncio.sleep_ms(1000)
            fu.wdt.feed()
        gc.collect()
        mem = gc.mem_free()
        print(f"{mem} bytes free")  # Print or wdt.feed() required. Lets print mem free.


if __name__ == '__main__':
    fu.init_watchdog()
    asyncio.run(start_main())
