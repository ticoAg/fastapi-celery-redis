# Usage

```sh
uv sync
# 1. 启动celery
celery -A tasks worker --loglevel=info -P eventlet --concurrency 30
# 2. 启动fastapi
python main.py
# 3. 启动flower监控
celery -A tasks flower
# 4. 启动并发测试
pytest test_api.py -s -v
```

# Note

这两天花了很多时间寻找合适的方案实现原生的

```
@celery_app.task
async def func()
```

操作, 直到看到这篇 blog, [[使用 Django 和 Celery 实现异步任务]](https://realpython.com/asynchronous-tasks-with-django-and-celery)
Revisit the Synchronous Code,重新审视同步代码,那些昂贵的同步操作,独立的任务,在任务处理流程中只需要触发一次调用操作即可继续进行后续流程的阻塞式任务(主要通过架构的形式解决阻塞问题)

这套技术很适合独立的任务,同时可以跟踪后续任务状态,便不必强行套上支持原生 async 的壳了

想要伪原生 `celery` + `async` + `redis` 直接使用 `fastapi`的`async` + `redis` 即可
