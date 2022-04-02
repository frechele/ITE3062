import streamlit as st

from timetabler.data.lecture_list import LectureList, Lecture


def show_report():
    st.title('수강평 남기기')

    lecture_list = LectureList()

    lecture_name = st.selectbox('과목명', lecture_list.get_lectures())
    professor_name = st.selectbox('교수명', lecture_list.get_professors_by_lecture(lecture_name))

    assignment_counts = st.select_slider(label='과제 수', options=['없음', '보통', '많음'])
    assignment_level = st.select_slider(label='과제 난이도', options=['쉬움', '보통', '어려움', '매우어려움'])
    team_project = st.select_slider(label='조별 활동', options=['없음', '있음'])
    exam_counts = st.select_slider(label='시험 횟수', options=['없음', '1번', '2번', '3번+'])
    exam_level = st.select_slider(label='시험 난이도', options=['쉬움', '보통', '어려움', '매우어려움'])
    exam_type = st.select_slider(label='시험 타입', options=['객관식', '혼합형', '논술형'])
    grade_level = st.select_slider(label='성적', options=['너그러움', '보통', '깐깐함'])

    if st.button('제출'):
        st.info('수강평을 추가하였습니다.')