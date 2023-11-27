import streamlit as st
import pymysql
import matplotlib.pyplot as plt
import pandas as pd
import register
import math
#from streamlit_modal import Modal

def write_cmt(cmt_input, post_no):
    conn = register.connect_mysql('CmtEditor')
    cur = conn.cursor()
    print(f'insert into PostComment(cmt_owner, create_date, cmt_text, post_no) values({st.session_state.user}, now(), BINARY({cmt_input}), {post_no} );')
    cur.execute(f'insert into PostComment(cmt_owner, create_date, cmt_text, post_no) values("{st.session_state.user}", now(), BINARY("{cmt_input}"), {post_no} );')
    conn.commit()
    conn.close()

def run():
    
    # conn = register.connect_mysql('PostEditor')
    # cur = conn.cursor(pymysql.cursors.DictCursor)
    # cur.execute('select count(post_no) as all_pages from PostPage;')
    # data = cur.fetchone()
    # print(data['all_pages'])
    # max_page = math.ceil(data['all_pages'] / 10)
    # max_id = data['all_pages']
    # print(max_id, max_page)
    # conn.commit()
    # conn.close()


    conn = register.connect_mysql('PostEditor')
    cur = conn.cursor(pymysql.cursors.DictCursor)
    st.markdown("---")
    print('query123') # https://stackoverflow.com/questions/948174/how-do-i-convert-from-blob-to-text-in-mysql
    #print(f'select post_no, post_title, post_owner_id, CONVERT(post_text using utf8) post_text from PostPage where post_no <= {max_id} and post_no >= {max(1, max_id - 10)} order by post_no desc;')
    cur.execute(f'select post_no, post_title, post_owner_id, CONVERT(post_text using utf8) post_text from PostPage order by post_no desc;')
    
    data = cur.fetchall() # 10 페이지에 대한 정보 긁어오기

    print('data', data)

    df = pd.DataFrame(data) # https://stackoverflow.com/questions/20638006/convert-list-of-dictionaries-to-a-pandas-dataframe
    df = df.style.hide(axis="index").data
    print('df', df)
    conn.commit()
    conn.close()

    for title_dict in data:
        st.header("게시글 제목")
        col1, col2 = st.columns(2)
        if len(title_dict['post_title']) > 10:
            title_dict['post_title'] = title_dict['post_title'][:10] + '...'
        if len(title_dict['post_owner_id']) > 10:
            title_dict['post_owner_id'] = title_dict['post_owner_id'][:10] + '...'
        
        with col1:
            st.subheader("게시글 번호")
            st.text(title_dict['post_no'])

        with col2:
            st.subheader("게시글 작성자")
            st.text(title_dict['post_owner_id'])

        # title_dict['post_title'], title_dict['post_text'], title_dict['post_no'], cmt['cmt_text']
        st.subheader(title_dict['post_title']) 
        st.text(title_dict['post_text'])
        st.markdown('---')
        # comment
        cmt_input = st.text_area(label = "댓글 내용", placeholder = '댓글을 입력하세요', key = f'text_area {title_dict['post_no']}') # https://discuss.streamlit.io/t/callbacks-how-to-get-current-control-value/15067
        print(cmt_input)
        if len(cmt_input) > 4:
            st.success("댓글 길이가 충분합니다.")
        elif len(cmt_input) == 0:
            st.error("댓글 내용이 필요합니다.")
        else:
            st.warning("댓글 내용은 5자 이상이 좋습니다.")
        st.button("댓글 작성", on_click = write_cmt, args = (cmt_input, title_dict['post_no']), disabled = len(cmt_input) < 2, key = f'cmt button {title_dict['post_no']}')

        st.markdown('---') # 존재하는 댓글 목록 나열
        conn = register.connect_mysql('CmtEditor')
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(f'select cmt_owner, create_date, convert(cmt_text using utf8) cmt_text from PostComment where post_no = {title_dict['post_no']};') # https://ydmny.tistory.com/entry/MSSQL-char-nchar-varchar-nvarchar-%EC%B0%A8%EC%9D%B4%EC%A0%90
        data = cur.fetchall()
        conn.commit()
        conn.close()
        print('cmt data', data)
        for cmt in data:
            print(cmt)
            cmt_owner = cmt['cmt_owner']
            create_date = cmt['create_date']
            st.subheader(f'작성자 {cmt_owner}({create_date})')
            st.write(cmt['cmt_text'])


    st.markdown("---")

if __name__ == '__main__':
    run()