import asyncio
from threading import Thread


def __func_init__(func, callback=None, except_callback=None, *a, **k):
    def func2():
        args = a
        kwargs = k
        try:
            result = func(*args, **kwargs)
            if callback:
                callback(result)
        except Exception as e:
            if except_callback:
                except_callback(e)

    return func2


async def __async_func_init__(func, callback=None, except_callback=None, *a, **k):
    async def func2():
        args = a
        kwargs = k
        try:
            result = await func(*args, **kwargs)
            if callback:
                await callback(result)
        except Exception as e:
            if except_callback:
                await except_callback(e)

    await func2()


async def __asyn_func__(func, callback=None, except_callback=None, *args, **kwargs):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, __func_init__(func, callback, except_callback, *args, **kwargs))


class __AsynFuncPool__:

    def __init__(self):
        self.thread_loop = asyncio.new_event_loop()
        self.run_loop_thread = Thread(target=self.start_loop)
        self.run_loop_thread.start()

    def start_loop(self):
        asyncio.set_event_loop(self.thread_loop)
        self.thread_loop.run_forever()

    def add_func(self, func, callback, except_callback, *args, **kwargs):
        asyncio.run_coroutine_threadsafe(__asyn_func__(func, callback, except_callback, *args, **kwargs),
                                         self.thread_loop)

    def add_async_func(self, func, callback, except_callback, *args, **kwargs):
        func = __async_func_init__(func, callback, except_callback, *args, **kwargs)
        asyncio.run_coroutine_threadsafe(func, self.thread_loop)

    def stop(self):
        self.add_func(self.thread_loop.stop, None, None)


asyn_func_pool = __AsynFuncPool__()
