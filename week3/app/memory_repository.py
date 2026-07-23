from typing import Optional
from app.repository import TaskRepository


class InMemoryTaskRepository(TaskRepository):
    def __init__(self):
        self.tasks: list[dict] = []

    def get_all(self) -> list[dict]:
        return self.tasks

    def get_by_id(self, task_id: int) -> Optional[dict]:
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None

    def create(self, title: str) -> dict:
        new_id = max((t["id"] for t in self.tasks), default=0) + 1
        new_task = {"id": new_id, "title": title, "done": False}
        self.tasks.append(new_task)
        return new_task

    def update(self, task_id: int, title: Optional[str], done: Optional[bool]) -> Optional[dict]:
        task = self.get_by_id(task_id)
        if task is None:
            return None
        if title is not None:
            task["title"] = title
        if done is not None:
            task["done"] = done
        return task

    def delete(self, task_id: int) -> bool:
        task = self.get_by_id(task_id)
        if task is None:
            return False
        self.tasks.remove(task)
        return True