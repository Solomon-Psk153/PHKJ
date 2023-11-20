import pickle
from pathlib import Path

import streamlit as st
import streamlit_authenticator as stauth
from IPython.display import display

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

file_path = Path(__file__).parent / "hashed_pw.pkl"

names = ["psk153"]
usernames = ["20183317"]

with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

credentials = {"usernames": {}}
for username, name, pw in zip(names, usernames, hashed_passwords):
    login_info = {"name": name, "password": pw}
    credentials["usernames"].update({username: login_info})
display(credentials)

authenticator = stauth.Authenticate(credentials, 
                "club", # 클라이언트에 저장될 json web token cookie(자격 증명 안해도 증명할 수 있음)
                "auth_club", # 랜덤키 (hatch cookie signature)
                cookie_expiry_days=0) # 비밀번호 입력 안해도 나 인것을 아는 기간

name, authentication_status, username = authenticator.login("로그인", "main")
display(authentication_status, name, username)
if authentication_status == False:
    st.error("아이디/비번이 일치하지 않음")
elif authentication_status == None:
    st.warning("아이디/비번을 입력하세요")
else:
    # 이제 여기서 부터 홈페이지 메인 구현
    st.title("Hi! i am streamlit web app")
    authenticator.logout("로그아웃", "main")