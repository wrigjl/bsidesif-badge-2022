from uasyncio import sleep_ms


async def blink(badge, cycles=10, c1="red", c2="red", c3="red", msg="Connection error..."):
    """Used to blink error codes while waiting for issue to resolve"""
    for second in range(0, cycles):
        badge.set_pixels(c1, c2, c3, write=True, lock_override=True)
        await sleep_ms(300)
        badge.set_pixels("off", "off", "off", write=True, lock_override=True)
        await sleep_ms(700)
        if second == 0 or second % 5 == 0:
            print(msg)


async def half_blink(badge, cycles=10, c1="red", c2="red", c3="red", msg="Connection error..."):
    """Used to blink error codes while waiting for issue to resolve"""
    for second in range(0, cycles):
        badge.set_pixels(c1, c2, c3, write=True, lock_override=True)
        await sleep_ms(150)
        badge.set_pixels("off", "off", "off", write=True, lock_override=True)
        await sleep_ms(350)
        if second == 0 or second % 5 == 0:
            print(msg)
