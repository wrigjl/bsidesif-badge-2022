import uasyncio as asyncio
import funcs as fu
from primitives.pushbutton import Pushbutton


def click(msg="SHORT"):
    print(f"{msg} click detected")


async def btn1():
    button = fu.button_pin
    pb = Pushbutton(button, suppress=True)

    pb.release_func(click, ("SHORT",))
    pb.double_func(click, ("DOUBLE",))
    pb.long_func(click, ("LONG",))

    await asyncio.sleep_ms(1000)


async def launch_btn_task():
    asyncio.create_task(btn1())
    while True:
        await asyncio.sleep_ms(10000)
        print(".")  # Required so watchdog doesn't time out


if __name__ == '__main__':
    asyncio.run(launch_btn_task())
