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
redis_host = os.getenv("REDIS_HOST", "192.168.31.179")
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


@celery_app.task(name="predict", bind=True)
async def predict(self, data):
    start_time = time.time()
    result = None
    timeout_occurred = False

    with Timeout(10, False):  # 设置 10 秒超时，不抛出异常
        gt = eventlet.spawn(async_task, self.request, data)
        result = await gt.wait()  # 等待异步任务完成

    if result is None and not timeout_occurred:
        # 超时或 wait() 返回 None 的情况
        result = {"error": "Task timeout or returned no result", "success": False}

    # 不管是否超时，都记录耗时
    cost = round(time.time() - start_time, 2)
    if isinstance(result, dict):
        result["cost"] = cost
    else:
        result = {"error": "Unexpected result type", "raw_result": str(result), "cost": cost, "success": False}

    return result
