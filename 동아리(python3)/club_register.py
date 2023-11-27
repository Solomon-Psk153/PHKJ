import streamlit as st
from pathlib import Path
import pymysql
import register
def register_request(radio_btn, uploaded_file, cur, conn):
    print('asdfasd', radio_btn)
    cur.execute(f'insert into who_in_the_club values("{st.session_state.user}", "{radio_btn}")')
    data = cur.fetchall()
    
    dir_name = st.session_state.user
    file_path = Path(__file__).parent / dir_name / 'register'

    for file in uploaded_file: # https://pydole.tistory.com/entry/Python-File-Copy-%ED%8C%8C%EC%9D%BC%EB%B3%B5%EC%82%AC
        with file_path.open(file.name, 'w') as f:
            f.write(file.read())
    conn.commit()
    conn.close()
    st.success("동아리 가입신청이 완료되었습니다.")
    
def run():
    st.title("동아리 신청")
    st.subheader("동아리 신청")
    
    conn = register.connect_mysql("ClubEditor")
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('select club_name from Club')
    data = cur.fetchall()
    print(data)
    club_tuple = tuple(club_dict['club_name'] for club_dict in data)
    radio_btn=st.radio("어느 동아리를 신청하시겠습니까?", options= club_tuple)

    # 파일 업로드
    uploaded_file = st.file_uploader("서류 업로드 (PDF, 문서 등):", type=["pdf", "docx"] , accept_multiple_files = True)
    
    # 서류 제출 버튼
    st.button("가입 신청", type = 'primary', on_click = register_request, args = (radio_btn, uploaded_file, cur, conn))

if __name__ == "__main__":
    run()