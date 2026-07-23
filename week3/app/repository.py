from abc import abstractmethod,ABC
from typing import Optional

class TaskRepository(ABC):
    @abstractmethod
    def get_all(self) ->list[dict]:
        ...
        
    @abstractmethod
    def get_by_id(self,task_id: int) -> Optional[dict]:
        ...
        
    @abstractmethod
    def create(self,title: str) -> dict:
        ...
        
    @abstractmethod
    def create(self,title: str) -> dict:
        ...
        
    @abstractmethod
    def update(self,task_id: int,title: Optional[str], done: Optional[bool]) -> Optional[dict]:
        ...
        
    @abstractmethod
    def delete(self,task_id: int) -> bool:
        ...