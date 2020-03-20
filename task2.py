import asyncio
import time

async def print_number():
    start = time.time()
    number = 0
    while True:
        print(number)
        number += 1
        await asyncio.sleep(1)
        duration = time.time() - start
        if int(duration) % 3 == 0:
            await print_duration(int(duration)) 


async def print_duration(duration):
    print(f"{duration} seconds have passed")


async def main():
    await print_number()

asyncio.run(main())