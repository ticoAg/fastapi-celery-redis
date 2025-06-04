import asyncio
import sys
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient

sys.path.append(Path(__file__).parents[1].as_posix())

from main import app

client = TestClient(app)


# 新增并发测试函数
@pytest.mark.asyncio
async def test_concurrent_start_task_async():
    """
    测试 /start-task-async 端点的并发能力
    """
    concurrent_num = 1000
    async with httpx.AsyncClient(base_url="http://localhost:8000", timeout=30) as ac:
        # 并发发送多个请求
        tasks = [ac.post("/start-task-async", json={"param": f"test-{i}"}) for i in range(concurrent_num)]
        responses = await asyncio.gather(*tasks)

        # 验证每个请求的响应状态码和内容
        for response in responses:
            assert response.status_code == 200
            assert "task_id" in response.json()
