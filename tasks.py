# -*- encoding: utf-8 -*-
"""
@Time    :   2025-05-30 18:00:07
@desc    :   定义的异步任务
@Author  :   ticoAg
@Contact :   1627635056@qq.com
"""

import asyncio
import os
import time

import celery_aio_pool as aio_pool
from celery import Celery
from dotenv import load_dotenv

assert aio_pool.patch_celery_tracer() is True

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
    # worker_pool="eventlet",  # 在启动命令中
)


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
async def predict(self, data):
    """支持异步 celery-aio-pool 目前不支持单进程多协程并发

    Args:
        data (Any obj can serialized): 输入数据

    Returns:
        dict: ...
    """
    tst = time.time()
    # result = await async_task(self.request, data)
    await asyncio.sleep(1)
    # result = sync_task(self.request, data)
    result = {}
    t_cost = round(time.time() - tst, 2)
    # result["cost_time"] = t_cost
    return result


@celery_app.task(name="funboost_predict", bind=True)
async def funboost_predict(self, data):
    """支持异步 celery-aio-pool 目前不支持单进程多协程并发

    Args:
        data (Any obj can serialized): 输入数据

    Returns:
        dict: ...
    """
    tst = time.time()
    # result = await async_task(self.request, data)
    await asyncio.sleep(1)
    # result = sync_task(self.request, data)
    result = {}
    t_cost = round(time.time() - tst, 2)
    # result["cost_time"] = t_cost
    return result
