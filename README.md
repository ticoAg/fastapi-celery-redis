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
python test_api.py -v
```
