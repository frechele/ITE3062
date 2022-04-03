import streamlit as st
import matplotlib.pyplot as plt


def show_timetable_wizard():
    st.title('시간표 마법사')

    fig_table = plt.figure(figsize=(1.5, 2))
    plt_table = fig_table.add_subplot(1, 1, 1)

    st.pyplot(fig_table)
