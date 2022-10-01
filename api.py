import ujson as json
from urequests import post as r_post
from urequests import get as r_get
import urandom
import neopixel
from machine import Pin


num_neo_pixels = 3
neop = neopixel.NeoPixel(Pin(4), num_neo_pixels)
button = Pin(0)


class Coms:

    INGEST_ENDPOINT = "/api/ingest/{}"
    REGISTER_ENDPOINT = "/api/unregister/{uid}"
    EVENT_PARTICIPATE_ENDPOINT = "/pull-lever/{uid}"

    def __init__(self, uid, badge_server=None, token=None):
        self.uid = uid
        self.token = token
        self.request = {}
        self.badge_server = badge_server if badge_server is not None else "https://ifhacker.meecles.net"
        self.auto_prediction = False
        self.custom_name = None
        self.prediction = []

        # For use with LED updates
        global neop
        self.np = neop
        self.display_colors = {
            'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255),
            'yellow': (245, 255, 0), 'purple': (255, 0, 255), 'orange': (250, 225, 0),
            'magenta': (255, 0, 20), 'teal': (0, 250, 120)
        }

    def _to_pix_color(self, color):
        # Reduce brightness and memory footprint
        divis = 5
        return int(color[0] / divis), int(color[1] / divis), int(color[2] / divis)

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
                    yield color
                n += 1

    def colors_to_rgb(self, c1, c2, c3):
        return [
            # Convert tuples into lists for use with API
            [c for c in self.display_colors[c1]],
            [c for c in self.display_colors[c2]],
            [c for c in self.display_colors[c3]]
        ]

    def set_pixels(self, c1, c2, c3, write=False):
        self.np[0] = self._to_pix_color(self.display_colors[c1])
        self.np[1] = self._to_pix_color(self.display_colors[c2])
        self.np[2] = self._to_pix_color(self.display_colors[c3])
        if write:
            self.write_pixels()

    def write_pixels(self):
        self.np.write()

    def gc(self):
        self.prediction = []
        self.custom_name = None

    def set_url(self, url):
        self.badge_server = url

    def badge_init(self):
        token = self.fetch()
        if token is None or len(token) < 1:
            print("No token stored, require registration")
            token = self.register()
        print("Loaded token!")
        self.token = token

    def register(self) -> str:
        url = "{}{}".format(self.badge_server, self.REGISTER_ENDPOINT.format(uid=self.uid))
        x = r_post(url)
        resp = x.json()
        if "success" not in resp or not resp["success"]:
            return ""
        if "token" not in resp:
            return ""
        print("Self-registered and saved API token for badge id: {}".format(self.uid))
        self.store(resp["token"])
        return resp["token"]

    def press(self):
        """Button on badge being pressed. Used to participate in event."""
        token = self.fetch()
        if not token or len(token) < 1:
            token = self.register()
        if token:
            self.request["token"] = token
        url = "{}{}".format(self.badge_server, self.EVENT_PARTICIPATE_ENDPOINT.format(uid=self.uid))
        print("Request: \n{}".format(json.dumps(self.request)))
        x = r_get(url, json=self.request)
        resp = x.json()
        print("Response: \n{}".format(json.dumps(resp)))

    def update_led_state(self, led0: list, led1: list, led2: list, badge_write=False, web_write=False):
        """LED Format [r: int, g: int, b: int]"""
        self.request = {
            "leds": [
                {"rgb": led0},
                {"rgb": led1},
                {"rgb": led2}
            ]
        }
        token = self.token
        if not token or len(token) < 1:
            print("No token found.. request miss")
        if token:
            self.request["token"] = token
        self._add_prediction()
        self._add_name()
        print("Stored LED state")
        if web_write:
            return self.write_led_state(badge_write=badge_write)
        return {}

    def write_led_state(self, badge_write=False):
        url = "{}{}".format(self.badge_server, self.INGEST_ENDPOINT.format(self.uid))
        print("Request: \n{}".format(json.dumps(self.request)))
        try:
            x = r_post(url, json=self.request)
            resp = x.json()
            print(resp)
            if resp["success"]:
                print("Updated LED status for: {}".format(self.uid))
                print("Server response: \n{}".format(json.dumps(resp)))
                if badge_write:
                    event_colors = resp["leds"] if resp["event_active"] else None
                    if resp["event_active"] and event_colors:
                        self.set_pixels(
                            event_colors[0]["name"],
                            event_colors[1]["name"],
                            event_colors[2]["name"],
                            write=True
                        )
                self.gc()
                return resp
            reason = resp["reason"] if "reason" in resp else None
            print("Failed to update led status: {}".format(reason) if reason else "Failed to update led.")
            self.gc()
            return resp
        except Exception as e:
            print(f"Server didn't respond. Defaulting to something else")
            self.gc()
            return {"event_active": False}

    def fetch(self, store_file=None) -> str:
        """fetch token associated with a UID"""
        if self.token is not None:
            return self.token
        uid = self.uid
        if store_file is None:
            store_file = "tokens.json"
        with open(store_file, "r") as file:
            data = json.load(file)
            return data[uid] if uid in data else ""

    def store(self, token, store_file=None):
        """Store received token associated with a UID"""
        uid = self.uid
        if store_file is None:
            store_file = "tokens.json"
        with open(store_file, "r") as file:
            data = json.load(file)
            data[uid] = token
        with open(store_file, "w") as file:
            file.write(json.dumps(data))
        return True

    def add_prediction_state(self, p0, p1, p2):
        leds = [p0, p1, p2]
        self.prediction = []
        for p in leds:
            if len(p) == 3:
                self.prediction.append({
                    "rgb": p
                })
            else:
                self.prediction.append({
                    "rgb": [0, 0, 0]
                })

    def set_auto_prediction(self, auto_prediction=True):
        self.auto_prediction = auto_prediction

    def _load_prediction(self):
        if self.auto_prediction:
            raise NotImplementedError("You gotta write this yourself :)")
        return self.prediction

    def _add_prediction(self):
        pre = self._load_prediction()
        if pre and len(pre) > 0:
            self.request["prediction"] = pre

    def set_name(self, name):
        self.custom_name = name

    def _add_name(self):
        if self.custom_name:
            self.request["name"] = self.custom_name
