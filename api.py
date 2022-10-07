from uasyncio import run as async_run

import ujson as json
import urequests as requests

<<<<<<< HEAD
import blinkers

=======
class Coms:
>>>>>>> main

class Coms:
    INGEST_ENDPOINT = "/api/ingest/{}"
    REGISTER_ENDPOINT = "/api/unregister/{uid}"
    EVENT_PARTICIPATE_ENDPOINT = "/pull-lever/{uid}"

    def __init__(self, uid, badge, badge_server=None, token=None):
        self.uid = uid
        self.token = token
        self.badge = badge
        self.request = {}
        self.badge_server = badge_server if badge_server is not None else "http://game.ifhacker.org"
        self.auto_prediction = False
        self.custom_name = None
        self.prediction = []

    def gc(self):
        self.prediction = []
        self.custom_name = None
        self.request = {}

    def set_url(self, url):
        self.badge_server = url

    def badge_init(self, simulate_failure=False):
        if simulate_failure:
            print("Badge init failed! (simulation)")
            return False
        try:
            token = self.fetch()
            if token is None or len(token) < 1:
                print("No token stored, require registration")
                token = self.register()
                if token == "":
                    print("Failed to register token. UUID already registered?")
                    return False
            print("Loaded token!")
            self.token = token
            return True
        except Exception as e:
            print("Badge init failed!")
            print(e)
            return False

    def register(self) -> str:
        url = "{}{}".format(self.badge_server, self.REGISTER_ENDPOINT.format(uid=self.uid))
        x = requests.post(url)
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
        try:
            x = requests.get(url, json=self.request)
            resp = x.json()
            print("Response: \n{}".format(json.dumps(resp)))
            resp["code"] = 0
            return resp
        except Exception as e:
            pass
        return {"success": False, "code": 1}

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
            x = requests.post(url, json=self.request)
            resp = x.json()
            print(resp)
            if resp["success"]:
                print("Updated LED status for: {}".format(self.uid))
                print("Server response: \n{}".format(json.dumps(resp)))
                if badge_write:
                    event_colors = resp["leds"] if resp["event_active"] else None
                    if resp["event_active"] and event_colors:
                        self.badge.set_pixels(
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
