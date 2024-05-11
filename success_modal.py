import base64
from streamlit.components.v1 import html
import streamlit as st
from web_backend import getUsername, getCurrentSliceNum

def sendMessageToBuddy(file, text):
    # 파일을 Base64로 인코딩
    if not file:
        return st.warning('인증 사진을 넣어주세요')

    base64_image = base64.b64encode(file.getvalue()).decode()
    image_url = f"data:image/jpeg;base64,{base64_image}"

    # 카카오 SDK 스크립트와 공유 버튼 생성 코드
    html_code = f"""
    <div id="kakaotalk-sharing-btn"></div>
    <script src="https://developers.kakao.com/sdk/js/kakao.min.js"></script>
    <script>
        Kakao.init('7476b316e9eedddc848473346eab3335'); // 앱 생성 시 받은 JavaScript 키 입력
        Kakao.Share.createDefaultButton({{
            container: '#kakaotalk-sharing-btn',
            objectType: 'feed',
            content: {{
                title: '{getUsername()}님의 {getCurrentSliceNum()-1}번째 한입 {st.session_state.nowGoal}의 인증이에요!',
                description: "{text}",
                imageUrl: "{image_url}",
                link: {{
                    mobileWebUrl: 'https://orengepage.onrender.com',
                    webUrl: 'https://orengepage.onrender.com',
                }},
            }},
        }});
    </script>
    """
    # Streamlit 페이지에 HTML 코드 삽입
    html(html_code, height=100)



@st.experimental_dialog("오늘의 한입을 사진과 글로 인증해요!")
def certifyModal():
    certify_file = st.file_uploader(label = '인증 사진을 업로드 해요', type=None, accept_multiple_files=False, key='Image Acceptor', help='도움글귀', on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
    certify_writing = st.text_input(label = '인증글을 작성해요', value = '오늘의 인증을 완성해요☺️')
    st.container(height=30, border=False)

    a,left_col,b, right_col,c = st.columns([1,5,1,5,1])
    with left_col:
        if st.button("카카오톡 인증하기"):
            sendMessageToBuddy(certify_file, certify_writing)
    with right_col:
        if st.button("나가기"):
            st.rerun()

