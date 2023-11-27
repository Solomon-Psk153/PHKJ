import streamlit as st
import pymysql
import register

def run():
    conn = register.connect_mysql('ClubEditor')
    cur = conn.cursor()
    cur.execute('select club_name, CONVERT(club_introduce, CHAR(255)) from Club')
    data = cur.fetchall()
    conn.commit()
    conn.close()
    
    st.header('동아리 목록')
    for club_name, club_introduce in data:
        st.subheader(club_name)
        st.write(club_introduce)