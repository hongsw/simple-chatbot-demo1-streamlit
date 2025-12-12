import streamlit as st
from openai import OpenAI

st.write("학교생활 비서 챗봇 - 서비스 v2")

# --- API KEY 입력 ---
api_key = st.text_input("🔑 OpenAI API Key 입력", type="password")
if not api_key:
    st.stop()

client = OpenAI(api_key=api_key)

# --- 대화 기록 초기화 ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Let's start chatting! 👇"}]

# --- UI 출력 ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 사용자 입력 ---
if prompt := st.chat_input("안녕하세요?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # --- ChatGPT 호출 ---
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages
        )
        answer = response.choices[0].message.content
        message_placeholder.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
