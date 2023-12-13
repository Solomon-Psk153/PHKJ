import streamlit as st
import register
import pymysql
from club_make import upload_file_to_server

def write_post(new_post_title, new_post_text, uploaded_file):#, modalWrite):
    conn = register.connect_mysql('PostEditor')
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(f'insert into PostPage(post_title, create_date, modify_date, delete_date, post_text, post_owner_id) values("{new_post_title}", now(), now(), null, binary("{new_post_text}"), "{st.session_state.user}");')
    for file in uploaded_file:
        path = f'/{st.session_state["user"]}/PostImages'
        cur.execute(f'select post_no from PostPage;')
        data = cur.fetchone()
        cur.execute(f'insert into Image_PostPage(Image_location, Image_post_no) values("/workspace/COM{path}/{file.name}", {data["post_no"]});')
        upload_file_to_server(path, file)
    conn.commit()
    conn.close()
    st.success("게시판 목록에서 확인해보세요")

def run():
    new_post_title = st.text_input(label = "게시물 제목", max_chars = 20)
    new_post_text = st.text_area(label = '게시물 내용', placeholder = "텍스트를 입력하세요")
    uploaded_file = st.file_uploader("사진 업로드", type=["png", "jpg", "jpeg", "gif"] , accept_multiple_files = True, key = "사진 업로드")
    st.button("게시물 게시", type = "primary", on_click = write_post, args = (new_post_title, new_post_text, uploaded_file))