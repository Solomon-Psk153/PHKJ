import streamlit as st
import register

def write_post(new_post_title, new_post_text):#, modalWrite):
    conn = register.connect_mysql('PostEditor')
    cur = conn.cursor()
    cur.execute(f'insert into PostPage(post_title, create_date, modify_date, delete_date, post_text, post_owner_id) values("{new_post_title}", now(), now(), null, binary("{new_post_text}"), "{st.session_state.user}");')
    conn.commit()
    conn.close()
    st.success("게시판 목록에서 확인해보세요")

def run():
    new_post_title = st.text_input(label = "게시물 제목", max_chars = 20)
    new_post_text = st.text_area(label = '게시물 내용', placeholder = "텍스트를 입력하세요")
    st.button("게시물 게시", type = "primary", on_click = write_post, args = (new_post_title, new_post_text))