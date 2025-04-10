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
    prompt = SYSTEM_PROMPT + f"\n{json.dumps(TODOS)}"

    return {"messages": [llm_with_tools.invoke([prompt] + state["messages"])]}

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