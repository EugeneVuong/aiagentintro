from langgraph.graph import START, END, StateGraph, MessagesState
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage
from langgraph_agent.tools import TODOS, add_todos, remove_todos
from langgraph_agent.prompts import SYSTEM_PROMPT
import json
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile", temperature=0
)
tools = [add_todos, remove_todos]
llm_with_tools = llm.bind_tools(tools)

# STORING MESSAGES
CONVERSATION = []

# FUNCTION TO CALL CHAT
# ... Implement Conversation Function

# Edges
def should_continue(state: MessagesState):
    pass

# Nodes
def chatbot(state: MessagesState):
    pass

tools = ToolNode(tools)

# Implement Graph Here
# ...