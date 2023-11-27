import streamlit as st
from streamlit_option_menu import option_menu
import site_introduce
import apply_for
import login
import register
import club_list
import board
import write_article

# def run():
st.markdown("""
<style>
.st-emotion-cache-czk5ss.e16jpq800
{
    visibility: hidden;
}
.st-emotion-cache-h5rgaw.ea3mdgi1
{
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

login_or_logout = ["로그인", "회원가입", "로그아웃"]
placeholder = st.empty()
if 'page' not in st.session_state:
    st.session_state.page = 0

with st.sidebar: # https://github.com/victoryhb/streamlit-option-menu
    choose = option_menu(
        menu_title ="COM",
        options = [login_or_logout[st.session_state.page], "우리 사이트에 대한 소개", "존재하는 동아리", "신청", "게시판 목록", "글쓰기"],
        icons=['bi bi-person-lock', 'bi bi-door-open', 'bi bi-list-task', 'bi bi-upload', 'bi bi-blockquote-left', 'bi bi-clipboard'],
        menu_icon="bi bi-menu-button", 
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "25px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#02ab21"},
        } # css 설정
    )

if choose == login_or_logout[st.session_state.page]:
    if st.session_state.page == 0:
        with placeholder.container():
            login.run()
    elif st.session_state.page == 1:
        with placeholder.container():
            print(st.session_state.page)
            register.run()
    # else:
        

elif choose == "우리 사이트에 대한 소개":
    site_introduce.run()

elif choose == "존재하는 동아리":
    if 'user' not in st.session_state:
        st.subheader("로그인하세요")
    else: club_list.run()

elif choose == "신청":
    if 'user' not in st.session_state:
        st.subheader("로그인하세요")
    else: apply_for.run()

elif choose == "게시판 목록":
    if 'user' not in st.session_state:
        st.subheader("로그인하세요")
    else: board.run()

elif choose == "글쓰기":
    if 'user' not in st.session_state:
        st.subheader("로그인하세요")
    else: write_article.run()