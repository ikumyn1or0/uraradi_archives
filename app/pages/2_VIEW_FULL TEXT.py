import streamlit as st
import pandas as pd
import glob
import re
import plotly.graph_objects as go

# set page config
st.set_page_config(page_title="裏ラジアーカイブス", page_icon="🦉")

########################
# describe page contents
########################

st.title("📻裏ラジアーカイブス🦉")

# ----------

st.header("書き起こしテキスト全文表示")

md_text1 = """
AIによって書き起こしたテキストを全文表示します。

「再生時間」のリンクに飛ぶことで、その回の再生時間からラジオを再生できます。
"""
st.markdown(md_text1)

# ----------

def create_yt_link(yt_url, text, time=None):
    yt_link = "https://youtu.be/" + re.search(r"v=(\S)+", yt_url).group()[2:]
    if time is None:
        pass
    else:
        yt_link = yt_link + "?t=" + str(time)
    return f'''<a href="{yt_link}">{text}</a>'''

csv_list = glob.glob("./input/*.csv")
date_list = []
for csv in csv_list:
    date_filename = csv.split("/")[-1]
    date_filename = date_filename.split(".")[0]
    if date_filename != "playlist_裏ラジオウルナイト":
        date_list.append(date_filename)

df_radio = pd.read_csv("./input/playlist_裏ラジオウルナイト.csv")
df_radio["is_transcripted"] = df_radio["date"].apply(lambda date: date in date_list)

title = st.selectbox("表示したい過去回を選択してください。", df_radio["title"])
if df_radio[df_radio["title"]==title].reset_index(drop=True).loc[0, "is_transcripted"]:
    filename = df_radio[df_radio["title"]==title].reset_index(drop=True).loc[0, "date"]
    url = df_radio[df_radio["title"]==title].reset_index(drop=True).loc[0, "url"]

    df_transcripted = pd.read_csv(f"./input/{filename}.csv")

    df_transcripted["second"] = df_transcripted["start_h"]*60*60 + df_transcripted["start_m"]*60 + df_transcripted["start_s"]
    df_transcripted["start"] = df_transcripted["start_h"].apply(lambda x: str(x).zfill(1)) + ":" + df_transcripted["start_m"].apply(lambda x: str(x).zfill(2)) + ":" + df_transcripted["start_s"].apply(lambda x: str(x).zfill(2))
    df_transcripted["link"] = df_transcripted.apply(lambda df: create_yt_link(url, df["start"], df["second"]), axis=1)
    df_transcripted = df_transcripted.sort_values(by="second", ascending=True)

    # st.write(df_transcripted[["link", "text"]].rename(columns={"link": "時間", "text": "書き起こしテキスト"}).to_html(escape=False, index=False), unsafe_allow_html=True)
    df_plot = df_transcripted[["link", "text"]].rename(columns={"link": "再生時間", "text": "テキスト"}).copy()
    fig = go.Figure(
        data=[
            go.Table(
                columnwidth=[1, 5],
                header=dict(
                    values=df_plot.columns.to_list()
                ),
                cells=dict(
                    values=df_plot.transpose(),
                    align=["center", "left"]
                )
            )
        ]
    )
    st.plotly_chart(fig, use_container_width=True)

else:
    st.markdown("この回はまだ書き起こしテキストを追加できていません......")
