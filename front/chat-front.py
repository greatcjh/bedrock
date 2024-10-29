import os
import streamlit as st
import requests

BACKEND_URL = os.environ.get('BACKEND_URL', 'http://backend-service:5000')

st.set_page_config(page_title="Chatbot") #HTML title
st.title("Chatbot") #page title


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

# 채팅 히스토리를 표시할 컨테이너
chat_container = st.container()

# 채팅 히스토리 표시
with chat_container:
    for message in st.session_state['messages']:
        st.write(message)

# 페이지 하단에 고정될 입력 폼
st.markdown(
    """
    <style>
    .stApp [data-testid="stVerticalBlock"] div:nth-child(5) {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: white;
        padding: 1rem;
        z-index: 1000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 입력 폼
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("Type your message here...", key='user_input')
    submit_button = st.form_submit_button(label='Send', on_click=send_message)