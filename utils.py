# -*- encoding: utf-8 -*-
"""
@Time    :   2025-06-05 10:02:04
@desc    :   https://stackoverflow.com/questions/70960234/how-to-use-asyncio-and-aioredis-lock-inside-celery-tasks/71067999#71067999
@Author  :   ticoAg
@Contact :   1627635056@qq.com
"""

import asyncio
import functools
from contextlib import contextmanager


@contextmanager
def temp_asyncio_loop():
    # asyncio.get_event_loop() automatically creates event loop only for main thread
    try:
        prev_loop = asyncio.get_event_loop()
    except RuntimeError:
        prev_loop = None
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        yield loop
    finally:
        loop.stop()
        loop.close()
        del loop
        asyncio.set_event_loop(prev_loop)


def with_temp_asyncio_loop(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        with temp_asyncio_loop() as t_loop:
            return f(*args, loop=t_loop, **kwargs)

    return wrapper


def await_(coro):
    return asyncio.get_event_loop().run_until_complete(coro)
