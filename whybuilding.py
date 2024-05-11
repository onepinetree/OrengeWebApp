from api_info import whybuilder_assistant_id
import streamlit as st
from openai import OpenAI
from chatbot_backend import sendMessagetoThread, runAndRetrieveData, getThreadId, saveChat
from api_info import API_KEY
from web_backend import getUsername


def app():

    client = OpenAI(api_key=API_KEY)
    openai_api_key = API_KEY

    #session_state에 저장해놓고 변수에 지정해놓은다.
    st.session_state.input_user_id = getUsername()
    st.session_state.input_thread_id = getThreadId(id = getUsername())

    input_user_id = st.session_state.input_user_id
    input_thread_id = st.session_state.input_thread_id

    st.title("💬 WhyBuilder")
    st.caption('🚀 와이빌더와 대화하고 목표를 구체화해요 \n목표를 향한 열정과 동기를 와이빌더에 저장해요.')

    if ("messages" not in st.session_state) or st.session_state.messages == []:
        st.session_state["messages"] = [{"role": "assistant", "content": "와이빌더에게 '안녕'이라고 인사를 건네주세요!"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if user_prompt := st.chat_input(): #변수를 할당받는 동시에, 할당받는 여부에 대한 bool을 return

        #인풋을 받은것을 session_state에 넣고 db에 저장하고 UI에 적는다.
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        saveChat(username = input_user_id,role = 'user',prompt = user_prompt)
        st.chat_message("user").write(user_prompt)

        #인풋을 보내고 답변을 받아온다.
        sendMessagetoThread(thread_id = input_thread_id,user_prompt = user_prompt)
        answer_prompt = runAndRetrieveData(
            assistant_id = whybuilder_assistant_id,
            thread_id = input_thread_id)
        
        #결과를 받은것을 session_state에 넣고 db에 저장하고 UI에 적는다.
        st.session_state.messages.append({"role": "assistant", "content": answer_prompt})
        saveChat(
            username = input_user_id,
            role = 'assistant',
            prompt = answer_prompt
            )
        st.chat_message("assistant").write(answer_prompt)