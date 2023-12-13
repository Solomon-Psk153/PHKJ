import pickle
from pathlib import Path
import streamlit as st
import bcrypt
import register
import pymysql
import time
# 0 
# 1
# 2
def selectpage(select): st.session_state.page = select
def restart(): st.session_state.page = 0

def run():
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
    st.markdown("<h1 style='text-align: center;'>로그인</h1>", unsafe_allow_html=True)
    with st.form(key = "login"):
        user_id = st.text_input(
            label = "아이디"
        )

        password = st.text_input(
            label = "비밀번호",
            type="password"
        )

        if st.form_submit_button(label = "로그인"):#, on_click = check_user, args = (user_id, password) )
                conn = register.connect_mysql('InfoEditor')
                cur = conn.cursor(pymysql.cursors.DictCursor)

                cur.execute(f'select passwd from Users where id = \'{user_id}\'')
                conn.commit()
                conn.close()

                result_user_passwd = cur.fetchone()

                if result_user_passwd == None:
                    print("result_user_passwd")
                    if user_id == '' or password == '':
                        st.warning("아이디와 비밀번호를 입력해주세요")
                    else:
                        st.error("해당 아이디는 존재하지 않습니다. 회원가입을 해주세요") 

                elif bcrypt.checkpw(password.encode('utf-8'), result_user_passwd['passwd'].encode('utf-8')):
                    st.success(f"{user_id}님, 환영합니다.")
                    time.sleep(1)
                    if 'user' not in st.session_state:
                        st.session_state["user"] = user_id
                else:
                    st.error("아이디와 비밀번호가 일치하지 않습니다.")

        st.form_submit_button(label = "회원가입", on_click = selectpage, args = (1, ))
        return