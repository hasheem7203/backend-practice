from fastapi import FastAPI ,HTTPException

app = FastAPI()


tasks = [{"id":1,"Title":"learn python basics","done":False},
         {"id":2,"Title":"learn python Advance","done":False},
         {"id":3,"Title":"learn react basics","done":True},
         {"id":4,"Title":"learn react Advance","done":False}]


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