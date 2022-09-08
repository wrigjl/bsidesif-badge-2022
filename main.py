import time
import funcs as fu
import spectre

polling_time = 30
polling_clock = polling_time * 1000
long_press = 2
long_clock = long_press * 1000
debounce = 20

def main_func(counter):
    if counter == 60000:
        counter = 0
    counter = counter + 1
    return counter

def test_wireless(wlan):
    if 'wlan' not in locals():
        print(f'wlan did not exist')
        wlan = fu.conn()
    if wlan.isconnected() == False:
        print(f'wlan is not connected')
        wlan.connect()
    return wlan

def test_func():
    countz = 0
    while True:
        print(f'Loop iteration {countz}')
        fu.npix_ran(fu.np)
        countz += 1
        if countz == 5:
            return 0

if __name__ == "__main__":
    that_time = time.ticks_ms()
    butt_counter = 0
    counter = 0
    wlan = fu.conn()
    while True:
        counter = main_func(counter)
        if counter % 5000 == 0:
            wlan = test_wireless(wlan)
        if counter % 15000 == 0:
            pass
        spectre.main_loop()
        # test_func()
        if time.ticks_diff(time.ticks_ms(), that_time) > polling_clock:
            fu.npix_ran(fu.np)
            that_time = time.ticks_ms()
            print(f'{polling_time} seconds have elapsed, time to check into the web server')
else:
   print("Executed when imported")