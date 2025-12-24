import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from test_agent2 import chatbot 

st.set_page_config(page_title="MSME & GST India Assistant", page_icon="🏢")

st.title("Vyappar-AI: MSME & GST Support Bot")

if "selected_chat" not in st.session_state:
    st.session_state.selected_chat = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.session_state.selected_chat is not None:
    start = st.session_state.selected_chat
    end = start + 2  # user + assistant

    for message in st.session_state.messages[start:end]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


if prompt := st.chat_input("Ask about Udyam registration, GST rates, etc."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Wait sir!"):
            try:
                initial_state = {"messages": [HumanMessage(content=prompt)]}
                response = chatbot.invoke(initial_state)
                full_response = response["messages"][-1].content

                st.markdown(full_response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )

            except Exception as e:
                st.error(f"Error: {str(e)}")
with st.sidebar:
    st.header("Previous Chats")

    if st.session_state.messages:
        for i in range(0, len(st.session_state.messages), 2):
            user_msg = st.session_state.messages[i]["content"]

            if st.button(user_msg[:20] + "...", key=f"chat_{i}"):
                st.session_state.selected_chat = i
                st.rerun()
    else:
        st.info("No previous chats yet.")

    st.divider()
    st.header("About")
    st.info("This bot is specialized for the Department of MSME and GST Council of India.")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.selected_chat = None
        st.rerun()
