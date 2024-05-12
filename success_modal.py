import base64
from streamlit.components.v1 import html
import streamlit as st
from web_backend import getUsername, getCurrentSliceNum

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
    certify_writing = st.text_input(label = '오늘의 후기를 작성해봐요')
    st.container(height=30, border=False)

    a,left_col,b, right_col,c = st.columns([1,5,1,5,1])
    with left_col:
        if st.button("달성완료"):
            sendMessageToBuddy(certify_file, certify_writing)
    with right_col:
        if st.button("취소"):
            st.rerun()

