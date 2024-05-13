import streamlit as st
import numpy as np
from web_backend import getUsername, getCurrentSlice, successRecord, skipRecord, getCurrentGoal, getCurrentSliceNum, getCurrentGoalField, passWeek, getSliceNum, getCurrentGoalNum, getCurrentSuccessRate, getComboRecord, getCurrentCombo, getCurrentSliceBoolList
from styles import styledText, welcomeText
from graph import draw_progress_bar
from success_modal import certifyModal, ReallySkipModal


def app():

    col1, col2, col3 = st.columns([1,2,2])
    with col1:  
        with st.container(height = 300, border=True):
            welcomeText()
            st.image('assests/orenge_icon.png', width=200)
    with col2: 
        with st.container(height = 300, border=True):
            st.title('오늘의 한입: ')
            st.subheader(f':orange[{getCurrentSlice()}]')
            st.write('')

            if st.button('달성완료!'):
                if getCurrentSlice() == '':
                    st.success("오늘의 한입이 없어요. '조각하기'에서 한입을 설정해주세요")
                else:
                    successRecord(getCurrentGoalNum())
                    if not getCurrentSliceBoolList()[-1] == True:
                        st.balloons()
                        st.toast('오늘의 한입 달성 성공!', icon = '🍊')
                        certifyModal()
                    else: 
                        passWeek()


            if st.button('SKIP'):
                if getCurrentSlice() == '':
                    st.success("오늘의 한입이 없어요. '조각하기'에서 한입을 설정해주세요")
                else:
                    if getCurrentSliceNum() == getSliceNum(week=getCurrentGoalNum()):
                        st.toast('조각의 마지막 한입은 스킵할 수 없어요😭')
                    else:
                        ReallySkipModal()
            
    with col3:
        with st.container(height = 300, border=True):
            #st.title(f'목표: {getCurrentGoal()}')
            styledText(
                            text =  f'조각: {getCurrentGoal()}',
                            size =  35,
                            color =  '#000000',
                            is_bold = True
                        )
            cur = getCurrentSliceNum()
            with st.container(height=180):
                st.session_state.bool_list = getCurrentSliceBoolList()
                for i in range(1,getSliceNum(week= getCurrentGoalNum())+1):
                    # 먼저 변수를 계산
                    current_goal_field = getCurrentGoalField()['slice_info'][i-1]
                    
                    # 계산된 변수를 f-string 안에서 사용
                    slice_string = f'{i}단계 한입 - {current_goal_field}'

                    if st.session_state.bool_list[i-1]:
                        styledText(text=slice_string, size=20, color='green', is_bold=True)
                    elif i == cur:
                        # 오렌지색 이모지와 함께 특별한 텍스트 강조
                        styledText(text=slice_string, size=20, color='orange', is_bold=True)
                    else:
                        styledText(text=slice_string, size=20, color='black', is_bold=True)


    col4, col5 = st.columns(2)
    with col4:
        fig = draw_progress_bar(getCurrentSuccessRate(), "프로젝트 진행률")  # fig 받기
        st.pyplot(fig)  # 스트림릿에 그래프를 표시
    with col5:
        fig = draw_progress_bar(getCurrentSuccessRate(), "프로젝트 진행률")  # fig 받기
        st.pyplot(fig)  # 스트림릿에 그래프를 표시

    data = np.random.rand(10,1)

    with st.container(border=False):
        col8, col7, col9 = st.columns([0.3,3,8])
        with col7:
            with st.container():
                st.write('')
                #st.subheader(f":orange[{getUsername()}]님의 열정온도는!")
                left_col, right_col = st.columns([1,1])
                x_data, y_data = getComboRecord()
                left_col.metric("한입 콤보", f"{getCurrentCombo()} 한입중")
                right_col.metric("조각 높이", f"{y_data[-1]} 조각", f"{getCurrentCombo()} 조각")
                left_col.container(height= 10, border=False)

                with st.expander('조각 높이 리워드 확인'):
                    with st.container(height=300):
                            st.write('높이 3 - 오랜지 성장')
                            st.write('높이 10 - 오랜지 성장')
                            st.write('높이 20 - 오랜지 성장')
                            st.write('높이 40 - 오랜지 성장')
                            st.write('높이 60 - 오랜지 성장')
                            st.write('높이 80 - 오랜지 성장')
                            st.write('높이 100 - ???')

                            

                #st.metric("다음 퀘스트", "캐릭터 Lv.5 로 진화", "1 조각")

        with col9: 
            st.container(height=15, border=False)
            with st.expander('나의 성장 그래프'):
                with st.container():
                    with st.container(height = 400, border=True):
                        st.subheader(f":orange[{getUsername()}]님의 성장!")
                        x_data, y_data = getComboRecord()
                        st.line_chart(y_data)      
                     


