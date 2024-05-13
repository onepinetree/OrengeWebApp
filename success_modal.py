import base64
from streamlit.components.v1 import html
import streamlit as st
from web_backend import passWeek, getCurrentSliceBoolList, getUsername, getCurrentSliceNum, skipRecord, getCurrentSlice, successRecord, getCurrentGoalNum
import datetime

def sendMessageToBuddy(file, text):
    if not file:
        return st.warning('인증 사진을 넣어주세요')

    base64_image = base64.b64encode(file.getvalue()).decode()
    image_url = f"data:image/jpeg;base64,{base64_image}"

    # 카카오톡 공유 기능을 바로 실행
    html_code = f"""
    <script src="https://developers.kakao.com/sdk/js/kakao.min.js"></script>
    <script>
        Kakao.init('7de421478d7cb865dd848740af8758d8'); // 앱 생성 시 받은 JavaScript 키 입력
        Kakao.Share.sendDefault({{
            objectType: 'feed',
            content: {{
                title: '{getUsername()}님의 {getCurrentSliceNum()-1}번째 한입 {st.session_state.nowGoal}의 인증이에요!',
                description: "{text}",
                imageUrl: "{image_url}",
                link: {{
                    mobileWebUrl: 'https://orengewebapp.onrender.com',
                    webUrl: 'https://orengewebapp.onrender.com',
                }},
            }}
        }});
    </script>"""
    
    html(html_code, height=0)  # 높이를 0으로 설정하여 보이지 않게 함



@st.experimental_dialog("오늘의 한입은 어떠셨나요?")
def certifyModal():
    #certify_file = st.file_uploader(label = '인증 사진을 업로드 해요', type=None, accept_multiple_files=False, key='Image Acceptor', help='도움글귀', on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
    user_input = st.text_input(label = '오늘의 후기를 작성해봐요')
    if  st.button('작성완료'):
        st.write(f"오늘의 한입 : {getCurrentSlice()}")  # 실제 내용으로 채울 부분
        st.write("인증여부 : 성공")
        st.write(f"인증일시 : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"인증글 : {user_input}")
    st.container(height=30, border=False)

    left_col, main_col, right_col = st.columns([1,1,1])
    with main_col:
        if st.button("달성완료"):
            successRecord(getCurrentGoalNum())
            st.toast('오늘의 한입 달성 성공!', icon = '🍊')
            if getCurrentSliceBoolList()[-1] == True:
                passWeek()
                st.rerun()
            else:
                st.rerun()



@st.experimental_dialog("😭정말 다음 한입으로 넘어가실껀가요?")
def ReallySkipModal():

    if st.button('다음 조각으로 넘어가기'):
        skipRecord()
        st.snow()
        st.rerun()



