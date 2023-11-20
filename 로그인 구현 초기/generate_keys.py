import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["psk153"]
usernames = ["20183317"]
passwords = ["superwise"]

hashed_passwords = stauth.Hasher(passwords).generate() # bcrypt

file_path = Path(__file__).parent / "hashed_pw.pkl" # 실행 파일 경로의 디렉터리에 이런 파일이름을 만든다

with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)