from langchain_core.tools import tool
from typing import List
import uuid


TODOS = []


@tool
def add_todos(todos: list[str]):
    pass

@tool
def remove_todos(ids: list[str]):
    pass