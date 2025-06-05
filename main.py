# -*- encoding: utf-8 -*-
"""
@Time    :   2025-05-30 17:59:37
@desc    :   fastapi服务
@Author  :   ticoAg
@Contact :   1627635056@qq.com
"""

import asyncio
import uuid

from celery.result import AsyncResult
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from tasks import celery_app, predict

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Embeddings"}


@app.post("/start-task")
async def start_task(data: dict):
    task = predict.delay(data)
    return {"task_id": task.id, "status": "pending"}


@app.get("/task/{task_id}")
async def get_task(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if not task_result:
        raise HTTPException(status_code=404, detail="Task not found")
    elif not task_result.ready():
        return JSONResponse(status_code=202, content={"task_id": str(task_id), "status": "Processing"})

    response = {
        "task_id": task_id,
        "status": task_result.state,
        "result": task_result.result if task_result.state == "SUCCESS" else None,
    }
    return response


@app.post("/start-task-async")
async def async_start_task(data: dict):
    await asyncio.sleep(0.5)
    uid = uuid.uuid4()
    return {"task_id": uid, "status": "done"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
