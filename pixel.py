import urandom


class Badge:

    def __init__(self, np):
        self.np = np
        self.pix_colors = {
            'red': (65, 0, 0), 'green': (0, 65, 0), 'blue': (0, 0, 65), 'yellow': (45, 55, 0),
            'purple': (65, 0, 65), 'magenta': (25, 0, 20), 'teal': (0, 25, 12), 'orange': (25, 10, 0)
        }
        self.display_colors = {
            'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255), 'yellow': (245, 255, 0),
            'purple': (255, 0, 255), 'orange': (250, 225, 0), 'magenta': (255, 0, 20), 'teal': (0, 250, 120)
        }
        self.color_array = [c for c in self.pix_colors]
        self.c1 = None
        self.c2 = None
        self.c3 = None

    def get_random_colors(self, event_colors=None):
        c1 = self.color_array[urandom.getrandbits(3)] if not event_colors else event_colors[0]["name"]
        c2 = self.color_array[urandom.getrandbits(3)] if not event_colors else event_colors[1]["name"]
        c3 = self.color_array[urandom.getrandbits(3)] if not event_colors else event_colors[2]["name"]
        return c1, c2, c3

    def colors_to_rgb(self, c1, c2, c3):
        return [
            # Convert tuples into lists
            [c for c in self.display_colors[c1]],
            [c for c in self.display_colors[c2]],
            [c for c in self.display_colors[c3]]
        ]

    def set_pixels(self, c1, c2, c3, write=False):
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        if write:
            self.write_pixels()

    def write_pixels(self):
        self.np[0] = self.pix_colors[self.c1]
        self.np[1] = self.pix_colors[self.c2]
        self.np[2] = self.pix_colors[self.c3]
        self.np.write()
