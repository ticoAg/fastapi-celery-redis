import asyncio
import json
import time

import aiohttp
import pytest


@pytest.mark.asyncio
async def test_send_request():
    async def send_request(session):
        url = "http://localhost:8000/start-task"
        payload = json.dumps({"sentences": ["Hello", "World"]})
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer sk-fhiJlbjt4ssZcChc4cF223AfF47744E9Af91A98e7cB3B238",
        }

        async with session.post(url, headers=headers, data=payload) as response:
            return await response.json()

    async def check_task_status(session, task_id):
        url = f"http://localhost:8000/task/{task_id}"
        async with session.get(url) as response:
            result = await response.json()
            return result

    start_time = time.time()  # 开始计时

    async with aiohttp.ClientSession() as session:
        num_requests = 3000  # 设置请求数量
        tasks = [send_request(session) for _ in range(num_requests)]
        responses = await asyncio.gather(*tasks)

    # 新增：轮询查询每个任务的状态，直到任务完成
    async with aiohttp.ClientSession() as session:
        for response in responses:
            task_id = response["task_id"]
            print(f"Checking task status for task_id: {task_id}")
            timeout = 30  # 设置超时时间
            interval = 1  # 每隔多少秒检查一次状态
            start_time = time.time()

            while True:
                status_response = await check_task_status(session, task_id)
                if status_response["status"] == "SUCCESS":
                    print(f"Task {task_id} completed successfully.")
                    # 验证返回结果是否符合预期格式
                    assert "result" in status_response, "Expected 'result' in response."
                    assert "sentences" in status_response["result"], "Expected 'sentences' in result."
                    assert "start_time" in status_response["result"], "Expected 'start_time' in result."
                    assert "finish_time" in status_response["result"], "Expected 'finish_time' in result."
                    break
                elif status_response["status"] == "FAILURE":
                    pytest.fail(f"Task {task_id} failed.")
                elif time.time() - start_time > timeout:
                    pytest.fail(f"Task {task_id} timed out.")

                await asyncio.sleep(interval)

    end_time = time.time()  # 结束计时
    total_time = end_time - start_time
    requests_per_second = num_requests / total_time

    print(f"Total time taken: {total_time:.2f} seconds")
    print(f"平均每秒处理的请求: {requests_per_second:.2f}")
    print(f"平均每个请求处理时间: {total_time / num_requests:.2f} seconds")
