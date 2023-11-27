import pickle
from pathlib import Path
import pymysql

import streamlit_authenticator as stauth

ids = ["psk153"]
nicknames = ["20183317"]
passwords = ["superwise"]

hashed_passwords = stauth.Hasher(passwords).generate() # bcrypt

# vi /etc/mysql/mysql.conf.d/mysqld.cnf
# https://sevendollars.tistory.com/238
conn = pymysql.connect(
    host = '54.180.124.30', # 껐다키면 계속 바꿤
    port = 52156, # 껏다키면 계속 바뀜
    user = 'testID',
    password = '',
    db = 'mysql',
    charset = 'utf8')

cur = conn.cursor(pymysql.cursors.DictCursor)
cur.execute('select host, user from user where user = \'testID\';')
result = cur.fetchall()
print(type(result), type([1]), type( (1,) ))
print(type(result) == type(tuple))
print(type(result) == type(list))
print(result)
conn.commit()
conn.close()

file_path = Path(__file__).parent / "hashed_pw.pkl" # 실행 파일 경로의 디렉터리에 이런 파일이름을 만든다

with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)