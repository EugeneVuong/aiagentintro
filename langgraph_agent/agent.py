from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import START, END, StateGraph, MessagesState
import datetime
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage
from typing import Literal
from langgraph_agent.tools import TODOS, add_todos, remove_todos
from langgraph.checkpoint.memory import MemorySaver
import json

llm = ChatGroq(
    model="llama-3.3-70b-versatile", temperature=0
)

tools = [add_todos, remove_todos]

llm_with_tools = llm.bind_tools(tools)

# STORING MESSAGES
CONVERSATION = []

# FUNCTION TO CALL CHAT
def send_message(message):
    CONVERSATION.append(HumanMessage(message))
    state = {
        "messages": CONVERSATION,
    }
    new_state = graph.invoke(state)
    print(TODOS)
    CONVERSATION.extend(new_state["messages"][len(CONVERSATION):])

# Edges
def should_continue(state: MessagesState):
    messages = state['messages']
    last_message = messages[-1]
    # If the LLM makes a tool call, then we route to the "tools" node
    if last_message.tool_calls:
        return "tools"
    # Otherwise, we stop (reply to the user)
    return END

# Nodes
def chatbot(state: MessagesState):

    SYSTEM_PROMPT = f"""
You are an AI assistant that manages a to-do list using the provided tools. Your goal is to help users add, remove, and display their to-dos efficiently.

## Tools Available:
1. `add_todos(todos: list[str])`
   - Adds new to-dos to the list.
   - Input: A list of to-do items (strings).
   - Output: The updated to-do list with each item containing `content`, `finished` status, and a unique `id`.

2. `remove_todos(ids: list[str])`
   - Removes to-dos by their unique IDs.
   - Input: A list of to-do item IDs (strings).
   - Output: The updated to-do list after removing specified items.

## Behavior Guidelines:
- When a user requests to **add tasks**, use `add_todos` with the provided task descriptions.
- When a user requests to **remove tasks**, use `remove_todos` with the IDs of the tasks to be deleted.
- When a user wants to **see the current to-do list**, return a list with just the bulletpoint, the content and status (Completed/Uncompleted).

## Example Interactions:
User: Add "Finish project report" and "Buy groceries" to my to-do list.
Assistant: Calling `add_todos(["Finish project report", "Buy groceries"])`

User: Remove the task with ID `123e4567-e89b-12d3-a456-426614174000`.
Assistant: Calling `remove_todos(["123e4567-e89b-12d3-a456-426614174000"])`

User: Show my to-do list.
Assistant:
* Finish project report - Uncompleted
* Buy groceries - Completed


LIST TODOS:
    {json.dumps(TODOS)}
"""


    
    return {"messages": [llm_with_tools.invoke([SYSTEM_PROMPT] + state["messages"])]}

tools = ToolNode(tools)

# Graph 
workflow = StateGraph(MessagesState)

# Add Nodes
workflow.add_node("chatbot", chatbot)
workflow.add_node("tools", tools)  # Add this line

# Add Edges
workflow.add_edge(START, "chatbot")
workflow.add_conditional_edges("chatbot", should_continue)
workflow.add_edge("tools", "chatbot")
graph = workflow.compile()