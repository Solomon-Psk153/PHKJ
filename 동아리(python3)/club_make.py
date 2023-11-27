import streamlit as st
from pathlib import Path
import pymysql
import register

def run():
    st.title("동아리 개설")

    # 동아리 정보 입력
    club_name = st.text_input("동아리 이름:")
    club_introduction = st.text_area("동아리 소개:", max_chars=100)

    if len(club_introduction) < 6: st.error("소개란은 반드시 작성해주세요(6자 이상)")

    # 파일 업로드
    uploaded_file = st.file_uploader("서류 업로드 (PDF, 문서 등):", type=["pdf", "docx"], accept_multiple_files = True, key = '동아리 개설')
    
    # 서류 제출 버튼
    if st.button("개설 신청"):
        if not club_name or not club_introduction:
            st.error("모든 필수 정보를 입력하세요.")
        else:
            st.success("동아리 개설 신청이 완료되었습니다. 검토 결과는 추후 공지드리겠습니다.")
            conn = register.connect_mysql("ClubEditor")
            cur = conn.cursor()
            cur.execute(f'insert into Club values("{club_name}", "{st.session_state.user}", binary("{club_introduction}"))')
            data = cur.fetchall()

            dir_name = f'{st.session_state["user"]}'
            file_path = Path(__file__).parent / dir_name / 'create_club'

            for file in uploaded_file: # https://pydole.tistory.com/entry/Python-File-Copy-%ED%8C%8C%EC%9D%BC%EB%B3%B5%EC%82%AC
                with file_path.open(file.name, 'w') as f:
                    f.write(file.read())
            conn.commit()
            conn.close()

if __name__ == "__main__":
    run()