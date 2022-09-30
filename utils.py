
import ubinascii
import network


def get_uuid():
    wlan_sta = network.WLAN(network.STA_IF)
    wlan_sta.active(True)
    wlan_mac = wlan_sta.config('mac')
    mac = ubinascii.hexlify(wlan_mac).decode()
    return "ebc626d8-6ddb-437c-8210-{}".format(mac)


if __name__ == '__main__':
    print(get_uuid())

