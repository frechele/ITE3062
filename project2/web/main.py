import streamlit as st
from PIL import Image
import time
import os
import uuid

from dataloader import generate_problems, ShowLevel, send_result


NUM_PROBLEMS = 12


def show_only_qa(problem):
    pass


def show_with_name(problem):
    st.write('등장 인물: {}'.format(', '.join(problem['qids'])))


def show_with_some_fact(problem):
    show_with_name(problem)

    st.markdown('**관련된 배경지식 목록**')

    sorted_fact = sorted(problem['facts'], key=lambda x: x['attn'], reverse=True)
    sum_of_attn = 0
    for pr in sorted_fact:
        fact = pr['fact']
        attn = pr['attn']

        sum_of_attn += attn

        st.write('{}'.format(fact, attn*100))
        if sum_of_attn > 0.5:
            break


def show_with_full_fact(problem):
    show_with_name(problem)

    st.markdown('**관련된 배경지식 목록**')
    for pr in problem['facts']:
        fact = pr['fact']
        attn = pr['attn']

        st.write('{} (중요도: {:.2f}%)'.format(fact, attn*100))


problem_show = {
    ShowLevel.ONLY_QA: show_only_qa,
    ShowLevel.WITH_NAME_SOME_FACT: show_with_some_fact,
    ShowLevel.WITH_NAME_FULL_FACT: show_with_full_fact
}


def start_and_clear_session():
    st.session_state['step'] = 0
    st.session_state['problems'] = generate_problems(NUM_PROBLEMS)
    st.session_state['correct'] = 0
    st.session_state['uuid'] = uuid.uuid1()
    st.session_state['start_time'] = time.time()


def get_current_problem():
    step = st.session_state['step']
    return st.session_state['problems'][step]


def progress_stage():
    problem, level = get_current_problem()
    duration = time.time() - st.session_state['start_time']
    is_correct = problem['answer'] == st.session_state['user_answer']
    
    if is_correct:
        st.session_state['correct'] += 1

    send_result(problem['confidence'], is_correct, level.value, duration, str(st.session_state['uuid']))

    if st.session_state['step'] < NUM_PROBLEMS - 1:
        st.session_state['step'] += 1
        st.session_state['start_time'] = time.time()
    else:
        st.session_state['step'] = -1

        st.info('맞춘문제: {}/{}'.format(st.session_state['correct'], NUM_PROBLEMS))


if __name__ == '__main__':
    if 'step' not in st.session_state:
        st.session_state['step'] = -1

    if st.session_state['step'] == -1:
        st.header('HCI project2 user study')

        st.write('본 user study에서는 인공지능이 제공하는 정보의 양과 질에 따른 사용성(usability)과 효율성(efficiency)을 측정하고자 합니다.')
        st.write('''아래 시작버튼을 누르면 총 {}문제가 나오며, 각 문제는 이미지와 이미지와 관련된 질문으로 구성되어 있습니다.
        일부 질문엔 문제를 해결하는데 참고할 수 있는 자료도 포함됩니다. 외부 자료를 참조하는 것은 지양해주시기 부탁드립니다.
        답을 낼 수 없다면 찍기보다는 모르겠음에 체크해주세요!'''.format(NUM_PROBLEMS))

        st.info('스크롤을 내려보면 힌트가 있을 수도 있고 없을 수도 있습니다.')

        st.button('시작', on_click=start_and_clear_session)
    else:
        problem, level = st.session_state['problems'][st.session_state['step']]

        img = Image.open(os.path.join('/data/senior', problem['key']))
        img = img.resize((448, 448))

        st.image(img)
        st.write('질문: {}'.format(problem['question']))

        st.session_state['user_answer'] = st.radio('답변', problem['top5'] + ['모르겠음'])
        st.button('다음', on_click=progress_stage)

        problem_show[level](problem)
