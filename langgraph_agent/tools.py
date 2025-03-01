from langchain_core.tools import tool
from typing import List
import uuid


TODOS = []


@tool
def add_todos(todos: list[str]):
    """Add new todos to the list"""
    for todo in todos:
        TODOS.append({
            "content": todo,
            "finished": False,
            "id": str(uuid.uuid4())
        })
    return TODOS


@tool
def remove_todos(ids: list[str]):
    """Remove todos by their IDs"""
    for todo_id in ids:
        TODOS[:] = [todo for todo in TODOS if todo["id"] != todo_id]
    return TODOS
