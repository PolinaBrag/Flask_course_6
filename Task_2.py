# from fastapi.params import Path
# from typing import List
# import uvicorn
# from fastapi import FastAPI
# from pydantic import BaseModel, Field
#
# tasks = []
#
# for i in range(10):
#     tasks.append({'title': f'title{i}', 'description': f'description{i}', 'status': True})
#
# app = FastAPI()
#
#
# class Tasks(BaseModel):
#     title: str = Field(max_length=32)
#     description: str = Field(max_length=200)
#     status: bool = Field(default=False)
#
#
# @app.get('/tasks/', response_model=List[Tasks])
# async def get_tasks():
#     return tasks
#
#
# @app.get("/task/{task_id}", response_model=Tasks)
# async def get_task(task_id: int = Path(..., ge=0, lt=len(tasks))):
#     return tasks[task_id]
#
#
# @app.post("/tasks/", response_model=Tasks)
# async def create_task(task: Tasks):
#     tasks.append(task)
#     return task
#
#
# @app.put("/task/{task_id}", response_model=Tasks)
# async def update_task(task_id: int, new_task: Tasks):
#     tasks[task_id] = new_task
#     return new_task
#
# @app.delete("/task/{task_id}", response_model=Tasks)
# async def delete_task(task_id: int):
#     return tasks.pop(task_id)
#
#
# uvicorn.run(app, host="127.0.0.1", port=8080)