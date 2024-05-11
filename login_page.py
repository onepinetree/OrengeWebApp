import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import auth

from datetime import datetime, timedelta
from chatbot_backend import createThread
import warnings
from web_backend import updateComboOnLogin
warnings.filterwarnings("ignore", category=UserWarning)

if not firebase_admin._apps:
    #cred = credentials.Certificate('orengewebapp-3c92d3f605ed.json')
    cred = credentials.Certificate('/etc/secrets/orengewebapp.json')
    app = firebase_admin.initialize_app(cred)

db = firestore.client()


def app():

    def logIn():
        try: 
            user = auth.get_user_by_email(email)
            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            #session_state에 user의 속성에서 받아온 계정정보를 임시로 저장
            if st.session_state.signedIn != True:
                updateComboOnLogin()

            st.session_state.signedIn = True
            #st.success('Login Succesful')

            #updateComboOnLogin()
        except:
            st.warning('Login Failed')
            


    def signUp(username: str, buddy_username:str):
        now = datetime.utcnow() + timedelta(hours=9)
        doc_ref = db.collection("user").document(username)
        doc_ref.set(
                    {
                    "signup_time": now.strftime("%Y-%m-%d-%H:%M"), 
                    "thread_id": createThread(), 
                    "username": username,
                    "total_goal_num" : 1,
                    "current_goal_num" : 1,
                    "orenge" : '',
                    "buddy_username" : buddy_username,
                        }
                    )
        users_ref = db.collection('user').document(username)
        goal_ref = users_ref.collection('goal_info').document('1_goal')
        goal_ref.set({
            'current_slice' : 1,
            'goal' : '',
            'slice_bool' : [False for i in range(7)],
            'slice_info' : ['' for i in range(7)],
            'slice_num' : 7,
        })



    col1, col2, col3 = st.columns([1,3,1])

    with col2:
        st.title('Hello')

        if not st.session_state.signedIn:
            choice = st.selectbox('Login/Signup', ['Login', 'Sign Up'])

            if choice == 'Login':
                email = st.text_input('Email Address')
                password = st.text_input('Password',type='password')
                #text_input에 type을 결정하게되면 그에 따라 인풋창이 약간 달라진다.
                st.button('Login', on_click=logIn)

            else:
                email = st.text_input('이메일')
                password = st.text_input('비밀번호',type='password')
                username = st.text_input('앞으로 사용하실 닉네임을 입력해주세요')
                buddy_username = st.text_input('버디의 닉네임을 입력해주세요')


                if st.button('회원가입 완료하기'):
                    try:
                        auth.create_user(email = email, password = password, uid = username)
                        signUp(username, buddy_username)
                        st.success('회원가입이 성공적으로 마무리 되었어요! 이제 로그인을 통해 시작해보아요')
                        st.balloons()
                    except:
                        st.warning('비밀번호가 6자리 이상이 아니거나 이미 있는 닉네임입니다.')
                       

                #선택바에서 선택한 값에 다르게 UI가 다르게 된다. 이걸 활용하면 입력창이 한번씩 나오는것도 구현 할 수 있지 않을까?
                #회원가입 요건 안맞으면 나오는 알림들도 구현해야함







