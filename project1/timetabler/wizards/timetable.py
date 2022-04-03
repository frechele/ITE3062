import streamlit as st
import matplotlib.pyplot as plt

from timetabler.data.time_table import LectureTimeDB


DIFFICULTY_LEVEL_LABELS = ['안정주의', '중립', '도전적']
TEAM_PROJECT_LABELS = ['싫어요', '중립', '좋아요']
EXAM_LEVEL_LABELS = ['쉬운게 좋아요', '중립', '나 빼고 다 못풀게 어려워라!']
DIST_LEVEL_LABELS = ['전공파이터', '중립', '교양을 쌓을래요', '다양한 경험을 할래요']


def show_timetable_wizard():
    st.title('시간표 마법사')

    difficulty_level = st.select_slider(label='이번학기 목표는?', options=DIFFICULTY_LEVEL_LABELS)
    difficulty_level = DIFFICULTY_LEVEL_LABELS.index(difficulty_level)

    team_project = st.select_slider(label='팀프로젝트는...', options=TEAM_PROJECT_LABELS)
    team_project = TEAM_PROJECT_LABELS.index(team_project)

    exam_level = st.select_slider(label='시험은...', options=EXAM_LEVEL_LABELS)
    exam_level = EXAM_LEVEL_LABELS.index(exam_level)

    dist_level = st.select_slider(label='저는...', options=DIST_LEVEL_LABELS)
    dist_level = DIST_LEVEL_LABELS.index(dist_level)

    lecture_list = LectureTimeDB()
    must_included = st.multiselect('이 과목은 꼭 들어야해요', lecture_list.get_lectures())

    if st.button('생성'):
        st.balloons()

        st.write(difficulty_level, team_project, exam_level, dist_level)
