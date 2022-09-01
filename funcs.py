from machine import SoftSPI, Pin, I2C, SPI
import neopixel
import time
import network
import secrets
import urandom

bit_depth = 5
num_neo_pixels = 3
np = neopixel.NeoPixel(Pin(4), num_neo_pixels)

def clear_pix(np, numpix):
    for i in range(numpix):
        np[i] = (0, 0, 0)
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
    return 0

# Cycle a pin several times to identify if it works properly...
def test_pin(num):
    pin_num = Pin(num, Pin.OUT)
    for each in range(10):
        pin_num.off()
        time.sleep(.25)
        pin_num.on()
        time.sleep(.25)

def set_cols(col_arr):
    request = urequests.put("http://game.ifhacker.org/update")

