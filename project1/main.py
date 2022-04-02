import streamlit as st

from wizards.timetable import show_timetable_wizard
from wizards.report import show_report


def show_main():
    st.title('Auto timetable maker')


if __name__ == '__main__':
    st.sidebar.title('Menu')
    button_status = [
        st.sidebar.button('시간표 마법사'),
        st.sidebar.button('수강평 남기기')
    ]

    menus = [
        show_timetable_wizard,
        show_report,
        show_main
    ]

    for i in range(len(menus)):
        if i == len(menus) - 1 or button_status[i]:
            menus[i]()
            break
