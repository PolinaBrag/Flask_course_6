from typing import List
import databases
import sqlalchemy
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field
from sqlalchemy import create_engine


DATABASE_URL = "sqlite:///mydatabase_2.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

tasks = sqlalchemy.Table("tasks",
metadata,
sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
sqlalchemy.Column("title", sqlalchemy.String(32)),
sqlalchemy.Column("description", sqlalchemy.String(128)),
sqlalchemy.Column("done", sqlalchemy.Boolean),
)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)


class TaskIn(BaseModel):
    id: int
    title: str = Field(max_length=32)
    description: str = Field(max_length=128)
    done: bool = Field(default=False)


class Task(BaseModel):
    id: int
    title: str = Field(max_length=32)
    description: str = Field(max_length=128)
    done: bool = Field(default=False)


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/fake_tasks/{count}")
async def create_note(count: int):
    for i in range(count):
        query = tasks.insert().values(title=f'title{i}',
                                      description=f'description{i}',
                                      done=True)
        await database.execute(query)
    return {'message': f'{count} fake tasks create'}


@app.get('/')
def root():
    return {'Message': 'index'}


@app.get("/tasks/", response_model=List[Task])
async def read_tasks():
    query = tasks.select()
    return await database.fetch_all(query)


@app.get("/task/{task_id}", response_model=Task)
async def read_task(task_id: int):
    query = tasks.select().where(tasks.c.id == task_id)
    return await database.fetch_one(query)


@app.post("/new_task/", response_model=Task)
async def create_task(task: TaskIn):
    query = tasks.insert().values(title=task.title, description=task.description, done=task.done)
    last_record_id = await database.execute(query)
    return {**task.dict(), "id": last_record_id}


@app.put("/update_task/{task_id}", response_model=Task)
async def update_task(task_id: int, new_task: TaskIn):
    query = tasks.update().where(tasks.c.id == task_id).values(**new_task.dict())
    await database.execute(query)
    return {**new_task.dict(), "id": task_id}


@app.delete("/del_task/{task_id}")
async def delete_task(task_id: int):
    query = tasks.delete().where(tasks.c.id == task_id)
    await database.execute(query)
    return {'message': 'Task deleted'}

uvicorn.run(app, host="127.0.0.1", port=8080)