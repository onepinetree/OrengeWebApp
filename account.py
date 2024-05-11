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


def app():

    def logOut():
        st.session_state.signedIn = False
        st.session_state.username = ''
        st.session_state.useremail = ''
        st.experimental_rerun()  # 페이지 리로드


    st.text('Name '+ st.session_state.username)
    st.text('Email id: ' + st.session_state.useremail)
    st.button('Sign out', on_click = logOut)

    st.header('사용법 동영상 임베딩')





















