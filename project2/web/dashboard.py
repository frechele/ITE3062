import streamlit as st
import requests
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def prepare_dataframe():
    result = json.loads(requests.get('http://127.0.0.1:8080/experiment-result').text)['result']
    df = pd.json_normalize(result)

    # calc zscore of spend time
    user_group = df.groupby('useruuid')
    mean_spendtime, std_spendtime = user_group['spendtime'].transform('mean'), user_group['spendtime'].transform('std')
    df['spendtime'] = (df['spendtime'] - mean_spendtime) / std_spendtime

    return df


if __name__ == '__main__':
    st.header('HCI2 project status')

    df = prepare_dataframe()

    st.dataframe(df)

    st.write('참여 인원: {}명'.format(len(df['useruuid'].unique())))

    fig = plt.figure()
    sns.kdeplot(data=df, x='spendtime', hue='infolevel')
    plt.xlabel('spendtime (zscore)')
    st.pyplot(fig)

    info_level_acc_group = df.groupby('infolevel')['correct']
    info_level_acc = info_level_acc_group.nunique() / info_level_acc_group.count()
    st.dataframe(info_level_acc)
