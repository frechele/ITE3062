import streamlit as st
from streamlit_option_menu import option_menu

from timetabler.wizards.timetable import show_timetable_wizard
from timetabler.wizards.report import show_report
from timetabler.wizards.view_report import show_view_report


if __name__ == '__main__':
    with st.sidebar:
        MENU_CHOOSED = option_menu('Timetabler', [
            '시간표 마법사', '수강평 남기기', '수강평 보기'
        ], icons=['kanban', 'book', 'easel'])

    if MENU_CHOOSED == '시간표 마법사':
        show_timetable_wizard()
    elif MENU_CHOOSED == '수강평 남기기':
        show_report()
    elif MENU_CHOOSED == '수강평 보기':
        show_view_report()
