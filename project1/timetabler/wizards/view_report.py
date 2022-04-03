import streamlit as st
from timetabler.data.lecture import Lecture

from timetabler.data.lecture import LectureList, LectureReport, LectureReportDB
import timetabler.data.lecture as L


def show_view_report():
    st.title('강의 정보')

    lecture_list = LectureList()
    db = LectureReportDB()

    lecture_name = st.selectbox('과목명', lecture_list.get_lectures())
    professor_name = st.selectbox(
        '교수명', lecture_list.get_professors_by_lecture(lecture_name))

    record = db.get_report(lecture_name, professor_name)

    st.write('과제 수 (없음 ↔ 많음)')
    st.progress(record.assignment_counts / (len(L.ASSIGNMENT_COUNTS_LABELS) - 1))

    st.write('과제 난이도 (쉬움 ↔ 매우어려움)')
    st.progress(record.assignment_level / (len(L.ASSIGNMENT_LEVEL_LABELS) - 1))

    st.write('시험 횟수 (없음 ↔ 3+)')
    st.progress(record.exam_counts / (len(L.EXAM_COUNTS_LABELS) - 1))

    st.write('시험 난이도 (쉬움 ↔ 매우어려움)')
    st.progress(record.exam_level / (len(L.EXAM_LEVEL_LABELS) - 1))

    st.write('시험 타입 (객관식 ↔ 주관식)')
    st.progress(record.exam_type / (len(L.EXAM_TYPE_LABELS) - 1))

    st.write('성적 (너그러움 ↔ 깐깐함)')
    st.progress(record.grade_level / (len(L.GRADE_LEVEL_LABELS) - 1))
