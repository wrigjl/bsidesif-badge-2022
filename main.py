import time
import funcs
import spectre

polling_time = 30
polling_clock = polling_time * 1000

def main_func():
    if 'wlan' not in locals():
        print(f'wlan did not exist')
        wlan = funcs.conn()
    if wlan.isconnected() == False:
        print(f'wlan is not connected')
        wlan = wlan.connect()

def test_func():
    countz = 0
    while True:
        print(f'Loop iteration {countz}')
        funcs.npix_ran(funcs.np)
        countz += 1
        if countz == 5:
            return 0

if __name__ == "__main__":
    print("Executed when ran directly")
    that_time = time.ticks_ms()
    while True:
        main_func()
        spectre.main_loop()
        test_func()
        if time.ticks_diff(time.ticks_ms(), that_time) > polling_clock:
            that_time = time.ticks_ms()
            print(f'{polling_time} seconds have elapsed, time to check into the web server')
else:
   print("Executed when imported")