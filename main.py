import funcs
import time
import spectre


def main_func():
    if 'wlan' not in locals():
        print(f'wlan did not exist')
        wlan = funcs.conn()
    if wlan.isconnected() == False:
        print(f'wlan is not connected')
        wlan = funcs.conn()
    

def test_func():
    countz = 0
    while True:
        print(f'Loop iteration {countz}')
        funcs.npix_ran(funcs.np)
        time.sleep(.25)
        countz += 1
        if countz == 15:
            return 0

if __name__ == "__main__":
    print("Executed when ran directly")
    while True:
        main_func()
        spectre.main_loop()
        test_func()
else:
   print("Executed when imported")