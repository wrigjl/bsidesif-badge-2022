from machine import SoftSPI, Pin, I2C, SPI
import neopixel
import time
import network
import secrets
import urandom
import urequests
import ujson

bit_depth = 5
num_neo_pixels = 3
np = neopixel.NeoPixel(Pin(4), num_neo_pixels)
pix_colors = {'red':(65, 0, 0), 'green':(0, 65, 0), 'blue':(0, 0, 65), 'yellow':(45, 55, 0), 'purple':(65, 0, 65), 'orange':(50, 25, 0)}
display_colors = {'red':(255, 0, 0), 'green':(0, 255, 0), 'blue':(0, 0, 255), 'yellow':(245, 255, 0), 'purple':(255, 0, 255), 'orange':(250, 225, 0)}

def clear_pix(np, numpix):
    for i in range(numpix):
        np[i] = (0, 0, 0)
    np.write()

def set_pix(np, pix_0, pix_1, pix_2):
    pix_0 = str(pix_0).lower()
    pix_1 = str(pix_1).lower()
    pix_2 = str(pix_2).lower()
    for each in [pix_0, pix_1, pix_2]:
        if each not in pix_colors:
            return 42
    np[0] = pix_colors[pix_0]
    np[1] = pix_colors[pix_1]
    np[2] = pix_colors[pix_2]
    np.write()

def pixel(np, parr1, parr2, parr3):
    np[0] = (parr1[0], parr1[1], parr1[2] )
    np[0] = (parr2[0], parr2[1], parr2[2] )
    np[0] = (parr3[0], parr3[1], parr3[2] )
    np.write()

def npix_ran(np):
    np[0] = ( int(urandom.getrandbits(bit_depth)) , int(urandom.getrandbits(bit_depth)) , int(urandom.getrandbits(bit_depth)) )
    np[1] = ( int(urandom.getrandbits(bit_depth)) , int(urandom.getrandbits(bit_depth)) , int(urandom.getrandbits(bit_depth)) )
    np[2] = ( int(urandom.getrandbits(bit_depth)) , int(urandom.getrandbits(bit_depth)) , int(urandom.getrandbits(bit_depth)) )
    np.write()

def fourpix_ran(np):
    pix_a = int(urandom.getrandbits(5))
    pix_b = int(urandom.getrandbits(5))
    pix_c = int(urandom.getrandbits(5))
    np[0] = ( pix_a , pix_b , pix_c , pix_a )
    np[1] = ( pix_c , pix_b , pix_a , pix_b )
    np[2] = ( pix_c , pix_a , pix_b , pix_c )
    np.write()

def conn():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    print(wlan.isconnected())
    return wlan

# Cycle a pin several times to identify if it works properly...
def test_pin(num):
    pin_num = Pin(num, Pin.OUT)
    for each in range(10):
        pin_num.off()
        time.sleep(.25)
        pin_num.on()
        time.sleep(.25)

# Requests URL needs to get UUID instead of this hard coded value, but currently we don't use it so it won't yet matter...
def set_colors(color_arr, uuid):
    for each in color_arr:
        if each not in display_colors:
            print('Somethign done got jacked...')
            return 42
    post_data = ujson.dumps({ "leds": [ { "rgb" : list(display_colors[color_arr[0]])}, 
    { "rgb" : list(display_colors[color_arr[1]])},
    { "rgb" : list(display_colors[color_arr[2]])}]})
    request_url = "http://game.ifhacker.org/api/ingest/1f025db3-281c-4b87-8153-4b64f9b27092"
    headers_value = {'content-type': 'application/json'}
    res = urequests.post(request_url, headers = headers_value, data = post_data)

def main_func():
    print(f'This is not supposed to run as a main module...')

if __name__ == "__main__":
   print("Executed when ran directly")
   main_func()
else:
   print("Executed when imported")