from fastapi import FastAPI ,HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None
    

tasks = []


@app.get("/")
def read_root():
    return { "name": "Task API",
            "version": "1.0",
            "endpoints": ["/tasks"] 
        }

@app.get("/health")
def health_status():
    return {"status ":"OK"}


@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"]==task_id:
            return task   
    raise HTTPException (status_code=404,detail=f"Task {task_id} not found " )

@app.post("/tasks",status_code=201)
def add_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400,detail="Title required")
    
    new_id = max((task["id"] for task in tasks), default=0 ) + 1
    new_task = {"id": new_id, "title": task.title,"done": False}
    tasks.append(new_task)
    return new_task


@app.put("/tasks/{task_id}",status_code=201)
def update_task(task_id: int ,update: TaskUpdate):
    for task in tasks:
        if task["id"]==task_id:
            if update.title is not None:
                if not update.title.strip():
                    raise HTTPException(status_code=400,detail="Titla cannot be empty")
                task["title"]=update.title
            if update.done is not None:
                task["done"] = update.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found" )


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")