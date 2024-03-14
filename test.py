import asyncio
import time
import pickle

import json
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

async def worker1():
    print('worker 1 is working')
    await asyncio.sleep(10)
    print('worker 1 is finish')
    return 'wrk 1'

async def worker2():
    print('worker 2 is working')
    await asyncio.sleep(3)
    print('worker 2 is finish')
    return 'wrk 2'

async def main():
    task_1 = asyncio.create_task(worker1())
    task_2 = asyncio.create_task(worker2())
    tasks = [task_1, task_2]
    for future in asyncio.as_completed(tasks):
        result = await future
        print(result)

if __name__ == "__main__":
    # asyncio.run(main())
    lst = [1,2,3]
    print(len(lst))