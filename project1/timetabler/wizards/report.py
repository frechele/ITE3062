import streamlit as st
from timetabler.data.lecture import Lecture

from timetabler.data.lecture import LectureList, LectureReport, LectureReportDB
import timetabler.data.lecture as L


def show_report():
    st.title('수강평 남기기')

    lecture_list = LectureList()

    lecture_name = st.selectbox('과목명', lecture_list.get_lectures())
    professor_name = st.selectbox(
        '교수명', lecture_list.get_professors_by_lecture(lecture_name))

    assignment_counts = st.select_slider(
        label='과제 수', options=L.ASSIGNMENT_COUNTS_LABELS)
    assignment_level = st.select_slider(
        label='과제 난이도', options=L.ASSIGNMENT_LEVEL_LABELS)
    team_project = st.select_slider(
        label='조별 활동', options=L.TEAM_PROJECT_LABELS)
    exam_counts = st.select_slider(label='시험 횟수', options=L.EXAM_COUNTS_LABELS)
    exam_level = st.select_slider(label='시험 난이도', options=L.EXAM_LEVEL_LABELS)
    exam_type = st.select_slider(label='시험 타입', options=L.EXAM_TYPE_LABELS)
    grade_level = st.select_slider(label='성적', options=L.GRADE_LEVEL_LABELS)

    if st.button('제출'):
        db = LectureReportDB()
        db.add_report(LectureReport(lecture=lecture_name, professor=professor_name, assignment_counts=assignment_counts, assignment_level=assignment_level,
                      team_project=team_project, exam_counts=exam_counts, exam_level=exam_level, exam_type=exam_type, grade_level=grade_level))
        db.summary_reports(lecture_list)

        st.info('수강평을 추가하였습니다.')
