import streamlit as st
import login_page, multi_app

st.set_page_config(
    page_title="OrengeWebApp",  # 웹 앱의 타이틀
    layout="wide",              # 레이아웃을 'wide'로 설정
)


def main():
    '''session_state의 생성 장소'''
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''
    if 'signedIn' not in st.session_state:
        st.session_state.signedIn = False
    if 'twicecheck' not in st.session_state:
        st.session_state.twicecheck = 2
    # session_state에 유저관리 정보와 로그인 관련 정보들에 대한 변수들의 설정 및 초기값 생성

    if st.session_state.signedIn == False:
        login_page.app()
    if st.session_state.signedIn == True:
        multi_app.MultiApp().run()

if __name__ == "__main__":
    main()
