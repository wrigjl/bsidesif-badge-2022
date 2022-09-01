import funcs
import time

funcs.conn()
countz = 0
while True:
    print(f'Loop iteration {countz}')
    funcs.npix_ran(funcs.np)
    time.sleep(.25)
    countz += 1
