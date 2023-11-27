import streamlit as st

st.title("동아리 가입 신청")

#여기에 동아리 개설 화면을 구성하는 요소들을 추가합니다.
club_name = st.text_input("동아리 이름")


if st.button("동아리 가입"):
    # 동아리 개설 로직을 추가합니다.
    st.success(f"{club_name} 동아리가 성공적으로 가입되었습니다!")

