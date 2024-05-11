import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import warnings
from web_backend import getUsername, getCurrentSlice, getCurrentSliceNum
warnings.filterwarnings("ignore", category=UserWarning)


if not firebase_admin._apps:
    cred = credentials.Certificate('orengewebapp-3c92d3f605ed.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()
users_ref = db.collection("user")


from streamlit.components.v1 import html



def app():



    def load_kakao_share():
        js_code = """
        <script src="https://t1.kakaocdn.net/kakao_js_sdk/2.7.1/kakao.min.js"
          integrity="sha384-kDljxUXHaJ9xAb2AzRd59KxjrFjzHa5TAoFQ6GbYTCAG0bjM55XohjjDT7tDDC01" crossorigin="anonymous"></script>
        <script>
          Kakao.init('c089c8172def97eb00c07217cae17495'); // 사용하려는 앱의 JavaScript 키 입력
        </script>
        
        <a id="kakaotalk-sharing-btn" href="javascript:shareMessage()">
          <img src="https://developers.kakao.com/assets/img/about/logos/kakaotalksharing/kakaotalk_sharing_btn_medium.png"
            alt="카카오톡 공유 보내기 버튼" />
        </a>
        
        <script>
          function shareMessage() {
            Kakao.Share.sendDefault({
              objectType: 'feed',
              content: {
                title: '딸기 치즈 케익',
                description: '#케익 #딸기 #삼평동 #카페 #분위기 #소개팅',
                imageUrl:
                  'http://k.kakaocdn.net/dn/Q2iNx/btqgeRgV54P/VLdBs9cvyn8BJXB3o7N8UK/kakaolink40_original.png',
                link: {
                  mobileWebUrl: 'https://developers.kakao.com',
                  webUrl: 'https://developers.kakao.com',
                },
              },
              social: {
                likeCount: 286,
                commentCount: 45,
                sharedCount: 845,
              },
              buttons: [
                {
                  title: '웹으로 보기',
                  link: {
                    mobileWebUrl: 'https://developers.kakao.com',
                    webUrl: 'https://developers.kakao.com',
                  },
                },
                {
                  title: '앱으로 보기',
                  link: {
                    mobileWebUrl: 'https://developers.kakao.com',
                    webUrl: 'https://developers.kakao.com',
                  },
                },
              ],
            });
          }
        </script>
        """
        html(js_code, height=200)

    def logOut():
        st.session_state.signedIn = False
        st.session_state.username = ''
        st.session_state.useremail = ''
        st.experimental_rerun()  # 페이지 리로드


    st.text('Name '+ st.session_state.username)
    st.text('Email id: ' + st.session_state.useremail)
    st.button('Sign out', on_click = logOut)

    st.header('사용법 동영상 임베딩')
    
    if st.button("카카오톡 공유하기"):
        load_kakao_share()





















