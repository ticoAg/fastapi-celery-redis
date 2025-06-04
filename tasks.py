# -*- encoding: utf-8 -*-
"""
@Time    :   2025-05-30 18:00:07
@desc    :   定义的异步任务
@Author  :   ticoAg
@Contact :   1627635056@qq.com
"""

import asyncio
import functools
import os
import time

import eventlet
import nest_asyncio
from celery import Celery
from dotenv import load_dotenv
from eventlet.timeout import Timeout

eventlet.monkey_patch()
nest_asyncio.apply()

load_dotenv(".env")

redis_password = os.getenv("REDIS_PASSWORD", "redis_QPJSSf")
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", 6379)
broker_url = f"redis://:{redis_password}@{redis_host}:{redis_port}/0"
backend_url = f"redis://:{redis_password}@{redis_host}:{redis_port}/0"


celery_app = Celery("task_executor")
celery_app.conf.update(
    broker_url=broker_url,
    result_backend=backend_url,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Shanghai",  # 使用东八区时间
    enable_utc=False,
    worker_pool="eventlet",  # 在启动命令中
)


def sync(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


async def async_task(request_param, data):
    # tid = request_param.id
    # logger.info(f"[TaskID: {tid}] started...")
    await asyncio.sleep(1)  # 使用 await 替代同步阻塞
    # logger.info(f"[TaskID: {tid}] finished...")
    return data


def sync_task(request_param, data):
    tid = request_param.id
    print(f"[TaskID: {tid}] started...")
    time.sleep(1)  # 使用 time.sleep 替代同步阻塞
    print(f"[TaskID: {tid}] finished...")
    return data


@celery_app.task(name="predict", bind=True)
def predict(self, data):
    """_summary_

    Args:
        data (Any obj can serialized): 输入数据

    Returns:
        dict: ...
    """
    tst = time.time()
    # result = async_task(self.request, data)
    result = sync_task(self.request, data)
    t_cost = round(time.time() - tst, 2)
    result["cost_time"] = t_cost
    return result
