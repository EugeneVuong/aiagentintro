
import streamlit as st
from langgraph_agent.agent import CONVERSATION, send_message
from langgraph_agent.tools import TODOS
from langchain_core.messages import HumanMessage


st.set_page_config(layout="wide")           

def submit_message():
    send_message(st.session_state["message"])

col1, col2 = st.columns(2)

with col1:
    st.subheader("Todos")

    for message in CONVERSATION:
        if type(message) == HumanMessage:
            with st.chat_message("user"):
                st.write(message.content)
        else:
            with st.chat_message("assistant"):
                st.write(message.content)
    
    message = st.chat_input("Type message here", on_submit=submit_message, key="message")


with col2:
    st.header("Todos")
    st.write(TODOS)