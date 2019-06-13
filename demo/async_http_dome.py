import aiohttp

from asyncio_func import async_func_pool


async def test(id, cookies, data):
    async with aiohttp.ClientSession(cookies=cookies) as session:
        print('开始请求')
        r = await post(session, 'https://m.dianping.com/isoapi/module', data=data)
        return [id, r]


async def get(session, *args, **kwargs):
    async with session.get(*args, **kwargs) as req:
        return await req.text()


async def post(session, *args, **kwargs):
    async with session.post(*args, **kwargs) as req:
        return await req.json()


async def callback(x):
    print(x)


async def except_callback(x):
    print(x)


if __name__ == '__main__':
    from_data = {"pageEnName": "shopList", "moduleInfoList": [{"moduleName": "mapiSearch", "query": {
        "search": {"start": 20, "categoryId": "10", "parentCategoryId": 10, "locateCityid": 0, "limit": 20,
                   "sortId": "0", "cityId": 9, "range": "-1", "maptype": 0, "keyword": ""}}}]}
    for x in range(1):
        async_func_pool.add_async_func(test, callback, None, x, from_data)
