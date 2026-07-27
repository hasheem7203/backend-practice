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
    conn = get_db()
    cursor=conn.cursor()
    cursor.execute("Select * from tasks")
    rows = cursor.fetchall()
    conn.close()
    return [{"id":r["id"], "title":r["title"],"done": bool(r["done"])} for r in rows]

@app.get("/tasks/{task_id}",summary="search task by id")
def get_task(task_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cur.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}
    
@app.post("/tasks",status_code=201,summary="create new task")
def add_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400,detail="Title required")
    
    conn =get_db()
    cursor=conn.cursor()
    cursor.execute("insert into tasks (title,done) values (?,?)",(task.title,0))
    
    conn.commit()
    new_id=cursor.lastrowid
    conn.close()
    
    return {"id":new_id,"title":task.title,"done":False}


@app.put("/tasks/{task_id}",status_code=201,summary="update a task")
def update_task(task_id: int ,update: TaskUpdate):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("select * from tasks where id = ?",(task_id,))
    row=cursor.fetchone()
    if row is None:
        conn.close()
        raise HTTPException (status_code=404,detail=f"Task {task_id} not found")
    
    new_title= row["title"]
    if update.title is not None:
        if not update.title.strip():
            conn.close()
            raise HTTPException (status_code=400,detail="Title cannot be empty")
    new_title = update.title
    new_done = row["done"]
    if update.done is not None:
        new_done= 1 if update.done else 0 
    
    cursor.execute("update tasks set title= ? , done = ? where id=?",(new_title,new_done,task_id))
    conn.commit()
    conn.close()
    return {"id": task_id,"Title":new_title,"Done":bool(new_done)}    

@app.delete("/tasks/{task_id}", status_code=204,summary="delete a task")
def delete_task(task_id: int):
    conn= get_db()
    cursor=conn.cursor()
    cursor.execute("select id from tasks where id = ?",(task_id,))
    row=cursor.fetchone()
    
    if row is None:
        conn.close()
        raise HTTPException(status_code=404,detail=f"Task {task_id} not found")
    
    cursor.execute("delete from tasks where id = ? ",(task_id,))
    conn.commit()
    conn.close()
    return

