from fastapi import FastAPI ,HTTPException
from pydantic import BaseModel
from typing import Optional
import sqlite3

DB_FILE = "tasks.db"

def get_db():
    conn =sqlite3.connect(DB_FILE)
    conn.row_factory= sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor=conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    
    cursor.execute("select count(*) from tasks")
    count=cursor.fetchone()[0]
    if count == 0:
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [("Buy groceries", 0), ("Finish assignment", 0), ("Walk the dog", 0)]
        )
        conn.commit()
        
    conn.close()
    
init_db()

app = FastAPI(
    title = "Task API",
    description="A simple CRUD API for managing a to do list",
    version="1.0.0"
)

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None
    

tasks = []


@app.get("/tasks",summary="liast all tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}",summary="search task by id")
def get_task(task_id: int):
    for task in tasks:
        if task["id"]==task_id:
            return task   
    raise HTTPException (status_code=404,detail=f"Task {task_id} not found " )

@app.post("/tasks",status_code=201,summary="create new task")
def add_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400,detail="Title required")
    
    new_id = max((task["id"] for task in tasks), default=0 ) + 1
    new_task = {"id": new_id, "title": task.title,"done": False}
    tasks.append(new_task)
    return new_task


@app.put("/tasks/{task_id}",status_code=201,summary="update a task")
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


@app.delete("/tasks/{task_id}", status_code=204,summary="delete a task")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")