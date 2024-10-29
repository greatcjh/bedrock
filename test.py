import os
import streamlit as st
import requests

# 환경 변수에서 BACKEND_URL을 가져오되, 없으면 기본값 사용
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://backend-service:5000')

st.title("Chat with Bot")

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

def send_message():
    user_input = st.session_state['user_input']
    if user_input:
        st.session_state['messages'].append(f"You: {user_input}")
        response = requests.post(f'{BACKEND_URL}/chat', json={'message': user_input})
        if response.status_code == 200:
            bot_response = response.json().get('message')
            st.session_state['messages'].append(f"Bot: {bot_response}")
        else:
            st.session_state['messages'].append("Bot: Error in response from server")
        st.session_state['user_input'] = ''

with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("Type your message here...", key='user_input')
    submit_button = st.form_submit_button(label='Send', on_click=send_message)

with st.expander("Chat History", expanded=True):  # 메시지를 스크롤 박스 안에 표시
    for message in st.session_state['messages']:
        st.write(message)
