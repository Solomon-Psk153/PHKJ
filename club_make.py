import streamlit as st
from pathlib import Path
import pymysql
import register
import os
import paramiko
import shutil
from pathlib import PureWindowsPath, PurePosixPath

def mkdir_p(sftp, dir_path):
    
    path_parts = dir_path.split('/')
    path_parts[0] = '/'
    for path_part in path_parts:
        print(path_part)
        try:
            sftp.chdir(path_part)
        except:
            sftp.mkdir(path_part)
            sftp.chdir(path_part)
            print('is make?')

def upload_file_to_server(dir_path, file): #(directroy, file):
    #https://velog.io/@wonjun12/Streamlit-%ED%8C%8C%EC%9D%BC-%EC%97%85%EB%A1%9C%EB%93%9C
    #https://sinaworld.co.kr/90
    
    # if not os.path.exists(directroy):
    #     os.makedirs(directroy)
    
    # with open(os.path.join(directroy, file.name), 'wb') as f:
    #     f.write(file.getbuffer()) # 로컬에 저장

    # https://colinch4.github.io/2023-09-07/13-30-00-450631/
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    dir_path = '/workspace/COM' + dir_path
    print(f'여기를 봐라 여기를 봐라 여기를 봐라 {dir_path}')
    
    # https://stackoverflow.com/questions/60291545/converting-windows-path-to-linux
    # path = PureWindowsPath(directroy)
    # print(path.parts)

    client.connect(
        hostname = '3.35.139.121', #'ec2-3-35-139-121.ap-northeast-2.compute.amazonaws.com',#'3.35.139.121',
        port = 55474,
        username = 'root',
        password = 'PR4J4cimfuC2xqLM2P7a') # SSH 설정에서 따로 발급받아야 함
    
    print('여기를 봐라 여기를 봐라 여기를 봐라')
    sftp = client.open_sftp()

    mkdir_p(sftp, dir_path)

    print('where', f"{dir_path + '/' + file.name}")
    with sftp.open(dir_path + '/' + file.name, 'wb') as f:
        f.write(file.getbuffer())

    sftp.close()
    client.close()

    return st.success(f"{file.name} 파일 저장 성공")

    

def run():
    st.title("동아리 개설")

    # 동아리 정보 입력
    club_name = st.text_input("동아리 이름:")
    if len(club_name) < 6: st.error("이름은 반드시 작성해주세요(6자 이상)")

    club_introduction = st.text_area("동아리 소개:", max_chars=100)

    if len(club_introduction) < 6: st.error("소개란은 반드시 작성해주세요(6자 이상)")

    # 파일 업로드
    uploaded_file = st.file_uploader("서류 업로드 (PDF, 문서 등)", type=["pdf", "docx"], accept_multiple_files = True, key = '동아리 개설')
    
    # 서류 제출 버튼
    if st.button("개설 신청"):
        if not club_name or not club_introduction:
            st.error("모든 필수 정보를 입력하세요.")
        else:
            conn = register.connect_mysql("ClubEditor")
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute('select club_name from Club')
            conn.commit()
            data = cur.fetchone()

            if  data != None and data['club_name'] == club_name:
                st.error("해당 동아리 이름이 이미 존재합니다. 다른 동아리 이름을 선택하세요")

            else:
                cur = conn.cursor()
                cur.execute(f'insert into Club values("{club_name}", "{st.session_state.user}", binary("{club_introduction}"))')
                dir_name = f'{st.session_state["user"]}'
                #file_path = Path(__file__).parent / dir_name / 'create_club_request_flies'
                # 위의 코드는 모든 윈도우 파일 경로에 dir_name, create_club_request_files를 추가한 것
                for file in uploaded_file:
                    upload_file_to_server(f'/{dir_name}/create_club_request_flies', file)

                conn.commit()
                conn.close()
                st.success("동아리가 개설 신청 완료되었습니다.")

if __name__ == "__main__":
    run()