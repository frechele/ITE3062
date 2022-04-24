import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from timetabler.data.lecture import LectureList, LectureReportDB

from timetabler.data.time_table import LectureTimeDB, TimeTable
from timetabler.optimizer.scoring import Evaluator


DIFFICULTY_LEVEL_LABELS = ['안정주의', '중립', '도전적']
TEAM_PROJECT_LABELS = ['싫어요', '중립', '좋아요']
EXAM_LEVEL_LABELS = ['쉬운게 좋아요', '중립', '나 빼고 다 못풀게 어려워라!']
DIST_LEVEL_LABELS = ['전공파이터', '중립', '교양을 쌓을래요', '다양한 경험을 할래요']
BLANK_LEVEL_LABELS = ['싫어요', '중립', '좋아요']


def draw_time_table(tt: TimeTable):
    fig = plt.figure(figsize=(10, 5.89))

    colors = ['pink', 'lightgreen', 'lightblue', 'wheat', 'salmon', 'orange', 'limegreen', 'plum']

    font = font_manager.FontProperties(fname='/usr/share/fonts/truetype/nanum/NanumGothicCoding.ttf').get_name()
    rc('font', family=font)

    for lecture_idx, lecture in enumerate(tt.lectures):
        for time in lecture.times:
            day = time.day - 0.48 + 1
            start = time.start / 2
            end = time.end / 2

            plt.fill_between((day, day+0.96), (start, start), (end, end), color=colors[lecture_idx % len(colors)], edgecolor='k', linewidth=0.5)
            plt.text(day+0.48, (start + end) * 0.5, '{}\n({})'.format(lecture.lecture, lecture.professor), ha='center', va='center', fontsize=8)

    ax = fig.add_subplot(111)
    ylim = ax.get_ylim()

    ax.yaxis.grid()
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(*ylim[::-1])
    ax.set_xticks(range(1, 6))
    ax.set_xticklabels(['월', '화', '수', '목', '금'])
    ax.set_ylabel('Time')

    ax2 = ax.twiny().twinx()
    ax2.set_xlim(ax.get_xlim())
    ax2.set_ylim(ax.get_ylim())
    ax2.set_xticks(ax.get_xticks())
    ax2.set_xticklabels(['월', '화', '수', '목', '금'])
    ax2.set_ylabel('Time')

    return fig


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

    blank_level = st.select_slider(label='공강은...', options=BLANK_LEVEL_LABELS)
    blank_level = BLANK_LEVEL_LABELS.index(blank_level)

    lecture_counts = st.slider(label='듣고 싶은 학점', value=[10, 21], max_value=30)

    lecture_list = LectureTimeDB()
    must_included = st.multiselect('이 과목은 꼭 들어야해요', lecture_list.get_lectures())

    if st.button('생성'):
        st.balloons()

        evaluator = Evaluator(LectureList(), LectureReportDB())

        timetabels = []

        tt = TimeTable()
        tt.add_lecture(lecture_list.get_timed_lecture_professor('시스템프로그래밍', '조영필')[0])
        tt.add_lecture(lecture_list.get_timed_lecture_professor('알고리즘문제해결기법', '채동규')[0])
        tt.add_lecture(lecture_list.get_timed_lecture('생명이란무엇인가?정신과물질')[0])
        tt.add_lecture(lecture_list.get_timed_lecture_professor('소프트웨어실무영어', '오연주')[2])
        tt.add_lecture(lecture_list.get_timed_lecture_professor('데이터베이스시스템및응용', '정형수')[0])
        tt.add_lecture(lecture_list.get_timed_lecture_professor('컴퓨터네트워크', '이춘화')[0])
        timetabels.append((tt, evaluator.evaluate(tt, difficulty_level, team_project, exam_level, dist_level, blank_level)))

        tt = TimeTable()
        tt.add_lecture(lecture_list.get_timed_lecture_professor('시스템프로그래밍', '조영필')[0])
        tt.add_lecture(lecture_list.get_timed_lecture_professor('알고리즘문제해결기법', '채동규')[0])
        tt.add_lecture(lecture_list.get_timed_lecture('생명이란무엇인가?정신과물질')[0])
        tt.add_lecture(lecture_list.get_timed_lecture_professor('소프트웨어실무영어', '오연주')[1])
        tt.add_lecture(lecture_list.get_timed_lecture_professor('데이터베이스시스템및응용', '정형수')[0])
        tt.add_lecture(lecture_list.get_timed_lecture_professor('컴퓨터네트워크', '이춘화')[0])
        timetabels.append((tt, evaluator.evaluate(tt, difficulty_level, team_project, exam_level, dist_level, blank_level)))

        tt = TimeTable()
        tt.add_lecture(lecture_list.get_timed_lecture_professor('시스템프로그래밍', '조영필')[0])
        tt.add_lecture(lecture_list.get_timed_lecture_professor('알고리즘문제해결기법', '채동규')[0])
        tt.add_lecture(lecture_list.get_timed_lecture('생명이란무엇인가?정신과물질')[0])
        tt.add_lecture(lecture_list.get_timed_lecture_professor('소프트웨어실무영어', '오연주')[1])
        tt.add_lecture(lecture_list.get_timed_lecture_professor('데이터베이스시스템및응용', '김상욱')[0])
        tt.add_lecture(lecture_list.get_timed_lecture_professor('컴퓨터네트워크', '이춘화')[0])
        timetabels.append((tt, evaluator.evaluate(tt, difficulty_level, team_project, exam_level, dist_level, blank_level)))

        timetabels.sort(key=lambda x: x[1], reverse=True)

        for tt, score in timetabels:
            st.subheader('시간표1 (점수: {:.2f})'.format(score))
            st.pyplot(draw_time_table(tt))
