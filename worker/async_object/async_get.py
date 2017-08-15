"""
CREAT: 2017/8/13
AUTHOR:　HEHAHUTU
"""
import asyncio
import time
from aiohttp import ClientSession
import concurrent.futures
import requests
from threading import Thread

"""
测试代码：
async def can_test(n):
    await asyncio.sleep(1)
    print(f'can test num: {n}')
async def main():
    start = time.time()
    await asyncio.wait([can_test(i) for i in range(10)])
    end = time.time()
    print(f'run need {end-start} second')
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
"""

url = 'http://114.55.64.68/service/getDeviceList.action'


def time_now():
    return time.time()


def get_url():
    html = requests.get(url)
    print(html.status_code)


def run_thread():
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(5000):
            executor.submit(get_url)
    end = time.time()
    print(end - start)


async def can_test(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            status = response.status
            print(status)


async def run_test():
    start = time.time()
    tasks = [
        can_test(url) for i in range(500)
        ]
    # await asyncio.wait()
    await asyncio.wait(tasks)
    end = time.time()
    print(f'run need {end-start} second')


def now_run():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_test())
    loop.close()


def more_worker(num):
    start = time.time()
    kk = num * 2
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(kk):
            executor.submit(now_run)

    end = time.time()
    print(f'get num: {num}K')
    print(end - start)


async def wrapped():
    async with ClientSession() as session:
        async with session.get(url) as response:
            status = response.status
            print(status)
    return status


async def inner(task):
    # print('inner: starting')
    # print('inner: waiting for {!r}'.format(task))
    result = await task
    print('inner: task returned {!r}'.format(result))
    return result


async def starter():
    st = time_now()
    print('starter: creating task')
    task = asyncio.ensure_future(wrapped())
    print('starter: waiting for inner')
    # ta = await inner(task)
    n = 100000
    tasks = [await inner(task) for i in range(n)]
    print(tasks)
    print(len(tasks))
    print('starter: inner returned')
    print(f'now get num: {n}')
    print(time_now()-st)

event_loop = asyncio.get_event_loop()
try:
    print('entering event loop')
    result = event_loop.run_until_complete(starter())
finally:
    event_loop.close()
