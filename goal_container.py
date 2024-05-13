import streamlit as st
from web_backend import getGoal, getSliceNum, getSlice, addSlice, deleteSlice, fixGoal, fixSlice
import time

@st.experimental_fragment
def goalContainer(week_num: int):
    '''몇번째주의 목표인지와 이 주는 몇개의 조각을 가지고 있는지를 받아 목표 컨테이너를 만들어준다.'''
    with st.container(border = True):
        st.subheader(f':orange[{week_num}번째 조각]')
        new_goal = st.text_input(
            #label = f"{week_num}번째 목표:",
            label = '',
            value =  f"{getGoal(week_num)}",
            key=f"{week_num}placeholder",
            )
        fixGoal(goalNum=week_num, newGoal=new_goal)

        #st.divider()
        st.write('')
        piece_num = getSliceNum(week_num)

        with st.expander('한입보기'):
            col1, col2 = st.columns(2)
            for i in range(1, piece_num + 1):
                # new_slice 값을 정의하기 위한 기본값 가져오기
                default_value = getSlice(week=week_num, slice=i)

                # i가 홀수일 경우 col1에, 짝수일 경우 col2에 입력 필드 배치
                if i % 2 != 0:
                    with col1:
                        new_slice = st.text_input(
                            label=f"{i}번째 한입:",
                            value=default_value,
                            key=f"{week_num}{i}placeholder",
                        )
                else:
                    with col2:
                        new_slice = st.text_input(
                            label=f"{i}번째 한입:",
                            value=default_value,
                            key=f"{week_num}{i}placeholder",
                        )
                fixSlice(goalNum=week_num, sliceNum=i, newSlice=new_slice)

            st.container(height = 20, border = False)

            with st.container(border = True):
                col3, col4, col5 = st.columns([1,1,1])
                with col3:
                    #st.button(label = '조각 추가', key = f'{week_num}add_button', on_click=addSlice(week_num))
                    st.button(label='한입 추가', key=f'{week_num}add_button', on_click=addSlice, args=(week_num,))
                with col4:
                    #st.button(label = '조각 삭제', key = f'{week_num}delete_button', on_click=deleteSlice(week_num))
                    st.button(label='한입 삭제', key=f'{week_num}delete_button', on_click=deleteSlice, args=(week_num,))
                with col5:
                    if st.button(label = '수정완료', key=f'{week_num}revise_button'):
                        time.sleep(1)
                        st.toast('한입이 수정 완료되었어요!', icon = '🍊')




            
