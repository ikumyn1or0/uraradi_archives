import streamlit as st
import pandas as pd
import glob
import re

# load dataset

csv_list = glob.glob("./input/*.csv")
date_list = []
for csv in csv_list:
    date_filename = csv.split("/")[-1]
    date_filename = date_filename.split(".")[0]
    if date_filename != "playlist_裏ラジオウルナイト":
        date_list.append(date_filename)

df_radio = pd.read_csv("./input/playlist_裏ラジオウルナイト.csv")
df_radio["link"] = '<a target="_blank" href='+df_radio["url"]+">"+df_radio["title"]+"</a>"
df_radio["is_transcripted"] = df_radio["date"].apply(lambda date: date in date_list)

selectbox_tuple = tuple(df_radio["title"])

# set page config

st.set_page_config(page_title="裏ラジアーカイブス", page_icon="🦉")

# describe page contents

st.title("📻裏ラジアーカイブス🦉")

st.header("書き起こしテキスト全文表示")

md_text1 = """
AIによって書き起こしたテキストを全文表示します。

「時間」のリンクに飛ぶことで、その回の再生時間からラジオを再生できます。
"""
st.markdown(md_text1)

title = st.selectbox("表示したい過去回を選択してください。", selectbox_tuple)
if df_radio[df_radio["title"]==title].reset_index(drop=True).loc[0, "is_transcripted"]:
    filename = df_radio[df_radio["title"]==title].reset_index(drop=True).loc[0, "date"]
    url = df_radio[df_radio["title"]==title].reset_index(drop=True).loc[0, "url"]
    url_id = re.search(r"v=(\S)+", url).group()[2:]

    df_transcripted = pd.read_csv(f"./input/{filename}.csv")

    df_transcripted["second"] = df_transcripted["start_h"]*60*60 + df_transcripted["start_m"]*60 + df_transcripted["start_s"]
    df_transcripted["start"] = df_transcripted["start_h"].apply(lambda x: str(x).zfill(1)) + ":" + df_transcripted["start_m"].apply(lambda x: str(x).zfill(2)) + ":" + df_transcripted["start_s"].apply(lambda x: str(x).zfill(2))
    df_transcripted["link"] = '<a target="_blank" href=https://youtu.be/'+url_id+"?t="+df_transcripted["second"].astype(str)+">"+df_transcripted["start"]+"</a>"
    df_transcripted = df_transcripted.sort_values(by="second", ascending=True)
    st.write(df_transcripted[["link", "text"]].rename(columns={"link": "時間", "text": "書き起こしテキスト"}).to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.markdown("この回はまだ書き起こしテキストを追加できていません。ごめんなさい……。")
