import streamlit as st
import pymysql
import bcrypt
import re
import dns.resolver

def connect_mysql(user):
    return pymysql.connect( # https://mxtoolbox.com/
            host = '3.35.139.121', # 껐다키면 계속 바꿤
            port = 54581, # 껏다키면 계속 바뀜
            user = user, #'testID',
            password = '',
            db = 'com',
            charset = 'utf8')

def run():
    st.markdown("<h1 style='text-align: center;'>회원 가입</h1>", unsafe_allow_html=True)
    with st.form(key = "register_form"):
        col1, col2 = st.columns(2)
        with col1:
            user_id = st.text_input(
                label = "아이디",
                placeholder = "사용자를 구별할 아이디를 입력하세요.",
                help = "사용할 아이디는 유일해야 합니다.(5자리 이상)"
            )

            password = st.text_input(
                label = "비밀번호",
                placeholder = "본인 인증에 필요한 비밀번호를 입력하세요.",
                help = "최대한 자신만이 알 수 있는 복잡한 비밀번호로 설정하세요.(5자리 이상)",
                type = "password"
            )

        with col2:
            nickname = st.text_input(
                label = "닉네임",
                placeholder = "실제로 활동할 별명을 입력하세요.",
                help = "5자리 이상"
            )

            re_check_password = st.text_input(
                label = "비밀번호 재입력",
                placeholder = "비밀번호를 재 입력하세요.",
                type = "password"
            )

        email = st.text_input(
            label = "이메일 주소",
            placeholder = "이메일 주소를 입력하세요."
        )

        phone = st.text_input(
            label = "전화번호",
            placeholder = "전화번호를 입력하세요."
        )

        #user_id, nickname, email, phone
        same = ["dummy"] # select한 결과가 리스트이면 중복되는 게 있다는 이야기이다
        if st.form_submit_button(label = "회원가입하기", type = "primary"): # 버튼을 누르고 중복이 없다는 것
            conn = connect_mysql('InfoEditor')
            cur = conn.cursor(pymysql.cursors.DictCursor)
            check_list_for_query = ["id", "phone", "email"]
            check_list_values = [user_id, phone, email]
            same.pop()

            for i in range(3):
                cur.execute(f'select {check_list_for_query[i]} from Users where id = \'{check_list_values[i]}\';')
                fetch_value = cur.fetchall()
                if len(user_id) > 5 and len(password) > 5 and len(nickname) > 5:
                    if type(fetch_value) != type( (1,) ): # 중복되는 것이 있다면
                        same.append(i)
                else:
                    st.warning("아이디, 비밀번호, 별명은 최소 5자리 이상입니다.")
                    same = ["dummy"]
                    break
            if password == re_check_password:
                st.success("비밀번호와 비밀번호 재입력이 일치합니다.")
            else:
                st.error("비밀번호와 비밀번호 재입력이 일치하지 않습니다.")

            p = re.compile('\d{3}-\d{4}-\d{4}')
            if p.match( phone ):
                st.success("전화번호가 형식에 맞습니다.")
            else:
                st.error("전화번호가 형식에 맞지않습니다.")
            
            # email

            p = re.compile('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$')

            if p.match( email ):
                st.success('이메일이 형식에 맞습니다.')
            else:
                st.error('이메일이 형식에 맞지않습니다.')

            if len(same):
                check_list_name = ["아이디", "전화번호", "이메일"]
                if same[0] != 'dummy':
                    for v in same:
                        st.error(f"{check_list_name[v]}(이)가 중복됩니다.")
                same = ["dummy"]
            else:
                st.success("중복되는 것이 없습니다.")
                # same = []

        rank = '일반'
        nickname += '(' + user_id + ')'
        print(same, rank, nickname)
        if len(same) == 0:
            hash_password = bcrypt.hashpw( password.encode('utf-8'), bcrypt.gensalt() )
            cur.execute('insert into Users values(%s, %s, %s, %s, %s, %s)',(user_id, rank, phone, email, hash_password , nickname))
            conn.commit()
            conn.close()
            st.success("회원가입 성공, 로그인 페이지로 이동합니다.")
            st.session_state.page = 0

if __name__ == '__main__':
    run()

# +----------+-----------+------+-----+---------+-------+
# | Field    | Type      | Null | Key | Default | Extra |
# +----------+-----------+------+-----+---------+-------+
# | id       | char(100) | NO   | PRI | NULL    |       |
# | rank     | char(100) | NO   |     | NULL    |       |
# | phone    | char(100) | YES  |     | NULL    |       |
# | email    | char(100) | YES  |     | NULL    |       |
# | passwd   | char(100) | NO   |     | NULL    |       |
# | nickname | char(100) | NO   | UNI | NULL    |       |
# +----------+-----------+------+-----+---------+-------+