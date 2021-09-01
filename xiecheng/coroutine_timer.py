import asyncio
import threading
import time


async def func1(a):
    while True:
        await asyncio.sleep(2)
        print(f"{threading.current_thread()}...{a}...{time.ctime()}")
        for i in range(10000):
            pass


async def func2():
    while True:
        await asyncio.sleep(2)
        print(f"func2__{threading.current_thread()}......{time.ctime()}")
        for i in range(10000):
            pass


async def main(tasks):
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main([func1("abc"), func2()]))