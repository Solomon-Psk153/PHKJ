import streamlit as st

# 페이지 전체의 스타일 설정
page_bg_color = """
    <style>
        body {
            background-color: #f0f5f5;
            color: #333;
            font-family: 'Arial', sans-serif;
        }
        .stApp {
            max-width: 800px;
            margin: 0 auto;
        }
        h1 {
            color: #3498db;
            text-align: center;
            margin-bottom: 30px;
        }
        h2 {
            font-size: 20px;
            color: #3498db;
            margin-bottom: 10px;
        }
        p {
            font-size: 16px;
            margin-bottom: 20px;
        }
        input, textarea {
            font-size: 16px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            margin-bottom: 20px;
            width: 100%;
        }
        button {
            background-color: #3498db;
            color: #fff;
            font-size: 18px;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
"""
st.markdown(page_bg_color, unsafe_allow_html=True)

def main():
    st.title("동아리 개설")

    # 섹션: 동아리 정보 입력
    st.markdown("## 동아리 정보 입력")
    club_name = st.text_input("동아리 이름:")
    club_introduction = st.text_area("동아리 소개:")

    # 섹션: 계획 보고서 업로드
    st.markdown("## 계획 보고서 업로드")
    st.file_uploader("계획 보고서 업로드 (PDF, 문서 등):", type=["pdf", "docx"])

    # 계획 보고서 내용 안내
    st.markdown("""
        ## 계획 보고서 작성 안내

        - **동아리 목표 및 목적**: 동아리를 만들기 위한 목표와 그 목표를 달성하기 위한 목적을 기술합니다.
        - **활동 계획**: 동아리의 주요 활동 내용과 일정을 작성합니다.
        - **회원 모집 계획**: 동아리 회원을 모집하기 위한 방법과 계획을 기술합니다.
        - **자금 운용 계획**: 동아리 활동을 위한 자금 운용 방안을 작성합니다.
    """)

    # 섹션: 개설 신청 버튼
    if st.button("개설 신청"):
        if not club_name or not club_introduction or not plan_report:
            st.error("모든 필수 정보를 입력하세요.")
        else:
            st.success("개설 신청이 완료되었습니다.")

if __name__ == "__main__":
    main()