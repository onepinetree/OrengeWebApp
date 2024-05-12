import streamlit as st
from streamlit_option_menu import option_menu
import home, account, piecing, whybuilding, buddy_board
from web_backend import getBuddyUsername, returnToMe

# 윗 배너의 타이틀 설정

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    @staticmethod
    def run():
        #updateComboOnLogin()
        # app = st.sidebar(
        with st.sidebar:        
            app = option_menu(
            #app도 optinon_menu를 통해서 input을 받는것.
                menu_title='OrengeWebApp ',
                options=['나의 오랜지','와이빌딩','조각하기','버디의 오랜지','Account'],
                icons=['house-fill','universal-access','sort-down','person-heart','person-circle'],
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
                    "icon": {"color": "white", "font-size": "23px"}, 
                    "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "orange"},
                    "nav-link-selected": {"background-color": "#02ab21"},}
                #일반/hover/선택 색을 지정해주는것도 포함되어있음.
                )
            
        #option_menu, 즉 app을 통해 받은 input에 따라서 지정하는 페이지
        if app == "나의 오랜지":
            returnToMe()
            home.app()
        if app == "Account":
            returnToMe()
            account.app()    
        if app == '조각하기':
            returnToMe()
            piecing.app()    
        if app == '와이빌딩':
            returnToMe()
            whybuilding.app() 
        if app == '버디의 오랜지':
            st.session_state.username = getBuddyUsername()
            buddy_board.app() 
