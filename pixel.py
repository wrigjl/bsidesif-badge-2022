import urandom
import neopixel
from machine import Pin

num_neo_pixels = 3
neop = neopixel.NeoPixel(Pin(4), num_neo_pixels)


class Badge:

    def __init__(self):
        global neop
        self.np = neop
        self.display_colors = {
            'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255),
            'yellow': (245, 255, 0), 'purple': (255, 0, 255), 'orange': (250, 225, 0),
            'magenta': (255, 0, 20), 'teal': (0, 250, 120), 'off': (0, 0, 0)
        }
        self.c1 = None
        self.c2 = None
        self.c3 = None
        self.lock_updates = False

    def _to_pix_color(self, color):
        # Reduce brightness and memory footprint
        divis = 5
        return int(color[0] / divis), int(color[1] / divis), int(color[2] / divis)

    def set_lock_updates(self, lock=True):
        self.lock_updates = lock

    def get_random_colors(self, event_colors=None):
        if event_colors:
            return (
                event_colors[0]["name"],
                event_colors[1]["name"],
                event_colors[2]["name"]
            )
        for i in range(0, 3):
            r = urandom.getrandbits(3)
            n = 0
            for color in self.display_colors:
                if r == n:
                    yield color if color != "off" else "teal"
                n += 1

    def colors_to_rgb(self, c1, c2, c3):
        return [
            # Convert tuples into lists for use with API
            [c for c in self.display_colors[c1]],
            [c for c in self.display_colors[c2]],
            [c for c in self.display_colors[c3]]
        ]

    def set_pixels(self, c1, c2, c3, write=False, lock_override=False):
        if self.lock_updates and not lock_override:
            return
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        if write:
            self.write_pixels(lock_override=lock_override)

    def secret_write(self, c1, c2, c3):
        self.np[0] = c1
        self.np[1] = c2
        self.np[2] = c3
        self.np.write()

    def write_pixels(self, lock_override=False):
        if self.lock_updates and not lock_override:
            return
        self.np[0] = self._to_pix_color(self.display_colors[self.c1])
        self.np[1] = self._to_pix_color(self.display_colors[self.c2])
        self.np[2] = self._to_pix_color(self.display_colors[self.c3])
        self.np.write()

    def clear_pix(self, numpix):
        for i in range(numpix):
            self.np[i] = (0, 0, 0)
        self.np.write()
