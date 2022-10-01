import uasyncio as asyncio
from machine import Pin
from primitives.pushbutton import Pushbutton


def click(msg="SHORT"):
    print(f"{msg} click detected")


async def btn1():
    button = Pin(0)
    pb = Pushbutton(button, suppress=True)

    pb.release_func(click, ("SHORT",))
    pb.double_func(click, ("DOUBLE",))
    pb.long_func(click, ("LONG",))

    await asyncio.sleep_ms(1000)


async def launch_btn_task():
    asyncio.create_task(btn1())
    while True:
        await asyncio.sleep_ms(10000)
        if __name__ == '__main__':
            import gc
            gc.collect()
            mem = gc.mem_free()
            print(f"{mem} bytes free")  # Print required so watchdog doesn't time out, so lets print memory free
        else:
            print(".")


if __name__ == '__main__':
    asyncio.run(launch_btn_task())
