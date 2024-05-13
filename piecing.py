import streamlit as st
from goal_container import goalContainer
from web_backend import getTotalGoalNum, addGoalObject, deleteGoalObject, getOrenge, setOrenge
from chat_bot import PieceChatBotUI



def app():

    col1, col2, col3 = st.columns([8,0.1,8])

    with col1:
        PieceChatBotUI()

    with col3:
        orenge = st.text_input(value=getOrenge(), label='🍊오랜지를 입력해 봐요.')
        setOrenge(orenge)

        with st.container():  # 중복 column을 사용하려면 col 내부에 컨테이너를 추가하고 그 안에서 col을 다시 추가해야함,
            with st.container(height = 600, border=True):
                
                container_num = getTotalGoalNum()

                for i in range(1, container_num + 1):
                    goalContainer(week_num=i)
                    st.container(height=20, border=False)

                col6, col7, col8, col9, col10 = st.columns([1,1,1,1,1])

                with col7:
                    st.button('조각 추가', on_click= addGoalObject)
                with col9:
                    st.button('조각 삭제', on_click= deleteGoalObject)
