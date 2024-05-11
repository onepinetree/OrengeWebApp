import streamlit as st
from web_backend import getUsername

def styleWelcome(username: str)->None:
    style_string = '''
    <style>
        .small-white { font-size: 22px; color: white; font-weight: bold; }
        .large-orange { font-size: 22px; color: #FFA500; font-weight: bold; }
    </style>
    '''
    st.markdown(style_string, unsafe_allow_html=True)
    # HTML에서 스팬 태그를 사용하여 각 텍스트 부분에 다른 클래스를 적용
    st.markdown(f'<p class="small-white">안녕하세요 <span class="large-orange">{username}</span>님!</p>', unsafe_allow_html=True)

def welcomeText()->None:
    # getUsername() 함수는 사용자의 이름을 반환하는 로직이어야 함
    styleWelcome(getUsername())

def styledText(text: str, size: int, color: str = 'white', is_bold: bool = True)-> None:
    unique_class = f"text-{size}-{color.replace('#', '')}"
    bold = "font-weight: bold;" if is_bold else ""
    style_string = f'<style>.{unique_class} {{ font-size: {size}px; color: {color}; {bold} }}</style>'
    st.markdown(style_string, unsafe_allow_html=True)
    st.markdown(f'<p class="{unique_class}">{text}</p>', unsafe_allow_html=True)
