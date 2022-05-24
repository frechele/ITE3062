import streamlit as st
from PIL import Image
import time
import os

from dataloader import generate_problems, ShowLevel


NUM_PROBLEMS = 16


def show_only_qa(problem):
    pass


def show_with_name(problem):
    pass


def show_with_some_fact(problem):
    pass


def show_with_full_fact(problem):
    pass


problem_show = {
    ShowLevel.ONLY_QA: show_only_qa,
    ShowLevel.WITH_NAME: show_with_name,
    ShowLevel.WITH_NAME_SOME_FACT: show_with_some_fact,
    ShowLevel.WITH_NAME_FULL_FACT: show_with_full_fact
}


if __name__ == '__main__':
    if 'step' not in st.session_state:
        st.session_state['step'] = -1

    if st.session_state['step'] == -1:
        st.header('HCI project2 user study')

        st.write('본 user study에서는 인공지능이 제공하는 정보의 양과 질에 따른 사용성(usability)과 효율성(efficiency)을 측정하고자 합니다.')
        st.write('''아래 시작버튼을 누르면 총 {}문제가 나오며, 각 문제는 이미지와 이미지와 관련된 질문으로 구성되어 있습니다.
        일부 질문엔 문제를 해결하는데 참고할 수 있는 자료도 포함됩니다. 외부 자료를 참조하는 것은 지양해주시기 부탁드립니다.
        답을 낼 수 없다면 찍기보다는 모르겠음에 체크해주세요!'''.format(NUM_PROBLEMS))

        if st.button('시작'):
            st.session_state['step'] = 0
            st.session_state['problems'] = problems = generate_problems(NUM_PROBLEMS)
            st.session_state['correct'] = 0
    else:
        problem, level = st.session_state['problems'][st.session_state['step']]

        img = Image.open(os.path.join('/data/senior', problem['key']))
        img = img.resize((448, 448))

        st.image(img)
        st.write('Question: {}'.format(problem['question']))

        start_time = time.time()

        if st.button('Next'):
            if st.session_state['step'] < NUM_PROBLEMS - 1:
                st.session_state['step'] += 1
            else:
                st.session_state['step'] = -1
