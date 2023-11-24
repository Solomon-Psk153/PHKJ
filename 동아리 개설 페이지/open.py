import streamlit as st

def main():
    st.title("동아리 개설")

    # 동아리 정보 입력
    club_name = st.text_input("동아리 이름:")
    club_introduction = st.text_area("동아리 소개:")

    # 파일 업로드
    uploaded_file = st.file_uploader("서류 업로드 (PDF, 문서 등):", type=["pdf", "docx"])


    # 서류 제출 버튼
    if st.button("개설 신청"):
        if not club_name or not club_introduction:
            st.error("모든 필수 정보를 입력하세요.")
        else:
            st.success("동아리 개설 신청이 완료되었습니다. 검토 결과는 추후 공지드리겠습니다.")

if __name__ == "__main__":
    main()