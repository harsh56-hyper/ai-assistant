import openai
import streamlit as st

st.title("AI ASSISTANT")

openai.api_key = st.secrets["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]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is your input?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    for response in openai.ChatCompletion.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    ):
        full_response += response.choices[0].delta.get("content", "")
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
