from typing import Optional 
from app.repository import TaskRepository
from app.db import get_connection,put_connection

class PostgreTaskRepository(TaskRepository):
    def get_all(self) -> list[dict]:
        conn= get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("select id , title , done from tasks order by id;")
                rows=cursor.fetchall()
                return [{"id": r[0], "title": r[1], "done": r[2]} for r in rows]
            
        finally:    
            put_connection(conn)
            
    def get_by_id(self, task_id: int) -> Optional[dict]:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, title, done FROM tasks WHERE id = %s;", (task_id,))
                row = cur.fetchone()
                return {"id": row[0], "title": row[1], "done": row[2]} if row else None
        finally:
            put_connection(conn)

    def create(self, title: str) -> dict:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO tasks (title, done) VALUES (%s, FALSE) RETURNING id, title, done;",
                    (title,)
                )
                row = cur.fetchone()
                conn.commit()
                return {"id": row[0], "title": row[1], "done": row[2]}
        finally:
            put_connection(conn)

    def update(self, task_id: int, title: Optional[str], done: Optional[bool]) -> Optional[dict]:
        existing = self.get_by_id(task_id)
        if existing is None:
            return None
        new_title = title if title is not None else existing["title"]
        new_done = done if done is not None else existing["done"]
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING id, title, done;",
                    (new_title, new_done, task_id)
                )
                row = cur.fetchone()
                conn.commit()
                return {"id": row[0], "title": row[1], "done": row[2]}
        finally:
            put_connection(conn)

    def delete(self, task_id: int) -> bool:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
                deleted = cur.rowcount > 0
                conn.commit()
                return deleted
        finally:
            put_connection(conn)
            