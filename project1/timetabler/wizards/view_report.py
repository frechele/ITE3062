import streamlit as st
from timetabler.data.lecture import Lecture

from timetabler.data.lecture import LectureList, LectureReport, LectureReportDB


def show_view_report():
    st.title('수강평 남기기')

    lecture_list = LectureList()

    lecture_name = st.selectbox('과목명', lecture_list.get_lectures())
    professor_name = st.selectbox(
        '교수명', lecture_list.get_professors_by_lecture(lecture_name))
