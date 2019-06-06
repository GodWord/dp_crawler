import asyncio
from abc import ABC

import requests
import tornado.ioloop
import tornado.web
import tornado.options
from tornado import gen
from tornado.httpserver import HTTPServer

tornado.options.parse_command_line()


def __func_init__(func, callback=None, except_callback=None, *a, **k):
    def func2():
        args = a
        kwargs = k
        try:
            result = func(*args, **kwargs)
            if callback:
                callback(result)
            return result
        except Exception as e:
            if except_callback:
                except_callback(e)
            return e

    return func2


async def func_to_async(func, callback=None, except_callback=None, *args, **kwargs):
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, __func_init__(func, callback, except_callback, *args, **kwargs))
    return r


def tset():
    req = requests.get('http://www.baidu.com')
    return req.text


class NoBlockingHnadler(tornado.web.RequestHandler, ABC):
    @gen.coroutine
    def get(self):
        r = yield func_to_async(tset)
        self.write(str(r))


def make_app():
    return tornado.web.Application([
        (r"/noblock", NoBlockingHnadler),
    ], )


if __name__ == "__main__":
    app = make_app()
    server = HTTPServer(app)
    server.bind(8889)
    server.start(0)
    tornado.ioloop.IOLoop.instance().start()