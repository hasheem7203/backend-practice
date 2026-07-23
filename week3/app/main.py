import os
from fastapi import FastAPI
from app.models import TaskCreate,TaskUpdate
from app.service import TaskService
from app.memory_repository import InMemoryTaskRepository
from app.postgres_repository import PostgreTaskRepository

app = FastAPI(
    title="Task API",
    description="CRUD API to manage a ToDo list",
    version="1.0.0"
)

REPOSITORY_TYPE = os.getenv("REPOSITORY_TYPE","memory")
repository = PostgreTaskRepository() if REPOSITORY_TYPE == "postgres" else InMemoryTaskRepository()
service = TaskService(repository)


@app.get("/tasks", summary= "list all tasks")
def get_tasks():
    return service.list_tasks()

@app.get("/tasks/{task_id}",summary="create new task")
def get_task(task_id:int):
    return service.get_task(task_id)

@app.post("/tasks",status_code=201,summary="Create New Task")
def add_task(task:TaskCreate):
    return service.create_task(task.title)

@app.put("/tasks/{task_id}",status_code=200,summary="Update A Task")
def update_task(task_id:int ,task:TaskUpdate):
    return service.update_task(task_id,task.title,task.done)

@app.delete("/tasks/{task_id}",status_code=204,summary="delete a task")
def delete_task(task_id:int):
    service.delete_task(task_id)
