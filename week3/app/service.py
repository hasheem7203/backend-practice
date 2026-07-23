from typing import Optional
from fastapi import HTTPException
from app.repository import TaskRepository

class TaskService:
    def __init__(self,repository: TaskRepository):
        self.repository=repository
        
    def list_tasks(self)->list[dict]:
        return self.repository.get_all()
    
    def get_task(self,task_id:int) ->dict:
        task = self.repository.get_by_id(task_id)
        if task is None:
            raise HTTPException(status_code=404,detail=f"Task {task_id} not found")
        return task
    
    def create_task(self,title:str) -> dict:
        if not title or not title.strip():
            raise HTTPException(status_code=400,detail="Title Required")
        return self.repository.create(title)
    
    def update_task(self,task_id: int ,title:Optional[str],done:Optional[bool]) -> dict:
        if title is not None and not title.strip():
            raise HTTPException(status_code=400,detail="title required")
        task = self.repository.update(title,done)
        if task is None:
            raise HTTPException(status_code=404,detail=f"Task {task_id} not found")
        return task
    def delete_task(self,task_id: int) -> None:
        deleted= self.repository.delete(task_id)
        if not deleted:
            raise HTTPException(status_code=404,detail=f"Task {task_id} not found")
        