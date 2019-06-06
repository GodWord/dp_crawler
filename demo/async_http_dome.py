import aiohttp

from demo.asyncio_func import asyn_func_pool


async def test(id):
    async with aiohttp.ClientSession() as session:
        r = await get(session, 'https://www.baidu.com')
        return [id, r]


async def get(session, *args, **kwargs):
    async with session.get(*args, **kwargs) as req:
        return await req.text()


async def callback(x):
    print(x)


async def except_callback(x):
    print(x)


for x in range(100):
    asyn_func_pool.add_async_func(test, callback, None, x)
