import funcs
import time
import spectre


def main_func():
    funcs.conn()

def test_func():
    countz = 0
    while True:
        print(f'Loop iteration {countz}')
        funcs.npix_ran(funcs.np)
        time.sleep(.25)
        countz += 1


if __name__ == "__main__":
   print("Executed when ran directly")
   main_func()
else:
   print("Executed when imported")