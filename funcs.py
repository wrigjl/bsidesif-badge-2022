import network
import ubinascii
import machine

import secrets

button_pin = machine.Pin(0)


def rst_cause(verbose=False):
    c = machine.reset_cause()
    if not verbose:
        return c
    if c == machine.PWRON_RESET:
        print(f"Power reboot {c}")
    elif c == machine.WDT_RESET:
        print(f"WDT reset {c}")
    elif c == 2:
        print(f"Fatal exception reset {c}")
    elif c == 3:
        print(f"WDT reset {c}")
    elif c == machine.SOFT_RESET:
        print(f"Soft reset {c}")
    elif c == machine.DEEPSLEEP_RESET:
        print(f"Deepsleep reset {c}")
    elif c == machine.HARD_RESET:
        print(f"Hard reset {c}")
    else:
        print(f"Unknown reset: {c}")
    return c  # Different actions depending on reset?


class WrapWDT:

    def __init__(self, disabled=False):
        self.disabled = disabled
        self.wdt = None

    def feed(self):
        if not self.disabled:
            self.wdt.feed()

    def launch(self):
        self.wdt = machine.WDT()
        self.disabled = False
        self.feed()


wdt = WrapWDT(disabled=True)


def init_watchdog():
    cause = rst_cause()
    launch = cause != 1
    # Launch if not a hardware WDT reset
    # HW WDT will still be enabled, Software disabled.
    print("\n\n")
    print("Launching software watchdog" if launch else "Skipping software watchdog launch")
    global wdt
    if launch:
        wdt.launch()
        wdt.feed()


# Updating neopixel values has been moved to pixel.py


def get_uuid():
    wlan_sta = network.WLAN(network.STA_IF)
    wlan_sta.active(True)
    wlan_mac = wlan_sta.config('mac')
    mac = ubinascii.hexlify(wlan_mac).decode()
    return "ebc626d8-6ddb-437c-8210-{}".format(mac)


def conn():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    # print(wlan.isconnected())
    return wlan


# Cycle a pin several times to identify if it works properly...
# def test_pin(num):
#     pin_num = Pin(num, Pin.OUT)
#     for each in range(10):
#         pin_num.off()
#         time.sleep(.25)
#         pin_num.on()
#         time.sleep(.25)
