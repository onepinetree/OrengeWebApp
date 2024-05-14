import streamlit as st
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
from streamlit.components.v1 import html
from chatbot_backend import setThreadId
from web_backend import getUsername


def auto_share_kakao():
    js_code = """
    
            <a id="kakaotalk-sharing-btn" href="javascript:;" onclick = "kakao()">
              <img src="https://developers.kakao.com/assets/img/about/logos/kakaotalksharing/kakaotalk_sharing_btn_medium.png"
                alt="카카오톡 공유 보내기 버튼" />
            </a>

            <script src="https://t1.kakaocdn.net/kakao_js_sdk/2.7.1/kakao.min.js"
                integrity="sha384-kDljxUXHaJ9xAb2AzRd59KxjrFjzHa5TAoFQ6GbYTCAG0bjM55XohjjDT7tDDC01" crossorigin="anonymous"></script>
            <script>
            function kakao(){
              Kakao.init('5ee6d3f7586bfec6cbc07ca8f29ebb47'); // 사용하려는 앱의 JavaScript 키 입력
              Kakao.Share.createDefaultButton({
                container: '#kakaotalk-sharing-btn',
                objectType: 'feed',
                content: {
                  title: '딸기 치즈 케익',
                  description: '#케익 #딸기 #삼평동 #카페 #분위기 #소개팅',
                  imageUrl:
                    'http://k.kakaocdn.net/dn/Q2iNx/btqgeRgV54P/VLdBs9cvyn8BJXB3o7N8UK/kakaolink40_original.png',
                  link: {
                    // [내 애플리케이션] > [플랫폼] 에서 등록한 사이트 도메인과 일치해야 함
                    mobileWebUrl: 'https:\/\/orengewebapp.onrender.com',
                    webUrl: 'https:\/\/orengewebapp.onrender.com',
                  },
                },
              });
              }
              kakao()
            </script>
    """
    html(js_code, height=200)

def logOut():
    st.session_state.signedIn = False
    st.session_state.username = ''
    st.session_state.useremail = ''
    st.experimental_rerun()  # 페이지 리로드


def app():

    st.text('이름: '+ st.session_state.username)
    st.text('이메일 주소: ' + st.session_state.useremail)
    st.button('로그아웃', on_click = logOut)

    #st.header('사용법 동영상 임베딩 -> 사진')

    if st.button('대화 내용 초기화 하기'):
        setThreadId(id = getUsername())
        st.session_state.slice_messages = []
        st.session_state.messages = []

    
    # if st.button("카카오톡 공유하기"):
    #     auto_share_kakao()


