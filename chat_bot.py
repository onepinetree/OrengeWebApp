import streamlit as st
from openai import OpenAI
from chatbot_backend import sendMessagetoThread, runAndRetrieveData, getThreadId, saveChat
from api_info import API_KEY, whybuilder_assistant_id, piecer_assistant_id
from web_backend import getUsername

@st.experimental_fragment
def ChatBotUI(title:str, caption:str, assistant_id:str, first_sentence):

    client = OpenAI(api_key=API_KEY)
    openai_api_key = API_KEY

    #session_state에 저장해놓고 변수에 지정해놓은다.
    st.session_state.input_user_id = getUsername()
    st.session_state.input_thread_id = getThreadId(id = getUsername())

    input_user_id = st.session_state.input_user_id
    input_thread_id = st.session_state.input_thread_id

    st.title(f"💬 {title}")
    st.caption(caption)

    if ("messages" not in st.session_state) or st.session_state.messages == []:
        st.session_state["messages"] = [{"role": "assistant", "content": first_sentence}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if user_prompt := st.chat_input(): #변수를 할당받는 동시에, 할당받는 여부에 대한 bool을 return

        #인풋을 받은것을 session_state에 넣고 db에 저장하고 UI에 적는다.
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        saveChat(username = input_user_id,role = 'user',prompt = user_prompt)
        #st.chat_message("user").write(user_prompt)

        #인풋을 보내고 답변을 받아온다.
        sendMessagetoThread(thread_id = input_thread_id,user_prompt = user_prompt)
        answer_prompt = runAndRetrieveData(
            assistant_id = assistant_id,
            thread_id = input_thread_id)
        
        #결과를 받은것을 session_state에 넣고 db에 저장하고 UI에 적는다.
        st.session_state.messages.append({"role": "assistant", "content": answer_prompt})
        saveChat(
            username = input_user_id,
            role = 'assistant',
            prompt = answer_prompt
            )
        st.chat_message("assistant").write(answer_prompt)


@st.experimental_fragment
def PieceChatBotUI():

    with st.container(height = 600,border=True):

        client = OpenAI(api_key=API_KEY)
        openai_api_key = API_KEY
        #session_state에 저장해놓고 변수에 지정해놓은다.
        st.session_state.input_user_id = getUsername()
        st.session_state.input_thread_id = getThreadId(id = getUsername(), num = 2)
        input_user_id = st.session_state.input_user_id
        input_thread_id = st.session_state.input_thread_id


        st.title("💬 조각 도우미")
        st.caption('🍋‍🟩 조각 도우미와 대화하고 막막한 목표를 일주일 단위의 조각, 하루 단위의 한입으로 조각내요.')

        left_dummy_col,chat_col,right_dummy_col = st.columns([1,100,1])

        if ("slice_messages" not in st.session_state) or st.session_state.slice_messages == []:
            st.session_state["slice_messages"] = [{"role": "assistant", "content": "조각 도우미에게 '안녕'이라고 인사를 건네주세요!"}]

        for msg in st.session_state.slice_messages:
            chat_col.chat_message(msg["role"]).write(msg["content"])

    if user_prompt := st.chat_input(): #변수를 할당받는 동시에, 할당받는 여부에 대한 bool을 return
        #인풋을 받은것을 session_state에 넣고 db에 저장하고 UI에 적는다.

        st.session_state.slice_messages.append({"role": "user", "content": user_prompt})
        saveChat(username = input_user_id,role = 'user',prompt = user_prompt)
        chat_col.chat_message("user").write(user_prompt)

        #인풋을 보내고 답변을 받아온다.
        sendMessagetoThread(thread_id = input_thread_id,user_prompt = user_prompt)
        answer_prompt = runAndRetrieveData(
            assistant_id = piecer_assistant_id,
            thread_id = input_thread_id)
        
        #결과를 받은것을 session_state에 넣고 db에 저장하고 UI에 적는다.
        st.session_state.slice_messages.append({"role": "assistant", "content": answer_prompt})
        saveChat(
            username = input_user_id,
            role = 'assistant_2',
            prompt = answer_prompt
            )
        chat_col.chat_message("assistant").write(answer_prompt)
