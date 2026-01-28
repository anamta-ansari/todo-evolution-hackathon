from sqlmodel import Session, select
from backend.models.task import Task
from backend.db.session import engine
from typing import Dict, Any, List


def add_task_tool(user_id: str, title: str, description: str = "") -> Dict[str, Any]:
    """Add a new task for the user"""
    with Session(engine) as session:
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            completed=False
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return {
            "task_id": task.id,
            "status": "created",
            "title": task.title
        }


def list_tasks_tool(user_id: str, status: str = "all") -> List[Dict[str, Any]]:
    """List user's tasks with optional status filter"""
    with Session(engine) as session:
        query = select(Task).where(Task.user_id == user_id)
        
        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)
        
        tasks = session.exec(query).all()
        
        return [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.complete,
                "created_at": task.created_at.isoformat()
            }
            for task in tasks
        ]


def complete_task_tool(user_id: str, task_id: int) -> Dict[str, Any]:
    """Mark a task as complete"""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        
        if not task or task.user_id != user_id:
            return {"error": "task not found or unauthorized"}
        
        task.complete = True
        session.commit()
        
        return {
            "task_id": task.id,
            "status": "completed",
            "title": task.title
        }


def delete_task_tool(user_id: str, task_id: int) -> Dict[str, Any]:
    """Delete a task"""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        
        if not task or task.user_id != user_id:
            return {"error": "task not found or unauthorized"}
        
        title = task.title
        session.delete(task)
        session.commit()
        
        return {
            "task_id": task_id,
            "status": "deleted",
            "title": title
        }


def update_task_tool(user_id: str, task_id: int, title: str = None, description: str = None) -> Dict[str, Any]:
    """Update task title or description"""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        
        if not task or task.user_id != user_id:
            return {"error": "task not found or unauthorized"}
        
        if title:
            task.title = title
        if description is not None:
            task.description = description
        
        session.commit()
        session.refresh(task)
        
        return {
            "task_id": task.id,
            "status": "updated",
            "title": task.title
        }