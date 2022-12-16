import streamlit as st
import pandas as pd
import plotly.express as px
import re
import plotly.graph_objects as go

# set page config
st.set_page_config(page_title="裏ラジアーカイブス", page_icon="🦉")

########################
# describe page contents
########################

st.title("📻裏ラジアーカイブス🦉")

# ----------

st.header("ラジオ過去回の情報")

# ----------

st.subheader("放送時間の時系列変化")

st.markdown("なお、放送時間に関する可視化において、総集編は除外しました。")

def create_yt_link(yt_url, text, time=None):
    yt_link = "https://youtu.be/" + re.search(r"v=(\S)+", yt_url).group()[2:]
    if time is None:
        pass
    else:
        yt_link = yt_link + "?t=" + str(time)
    return f'''<a href="{yt_link}">{text}</a>'''

df_radio = pd.read_csv("./input/playlist_裏ラジオウルナイト.csv")
df_radio = df_radio[~df_radio["number"].str.contains("総集編")].reset_index(drop=True)
df_radio["hour"] = (df_radio["length"]/3600).round(2)
df_radio["caption"] = df_radio["number"].apply(lambda x: x[3:])
df_radio["link"] = df_radio.apply(lambda df: create_yt_link(df["url"], df["title"]), axis=1)

fig = px.line(df_radio, x="date", y="hour", text="caption", markers=True, labels={"date": "放送日付", "hour": "放送時間(h)", "caption": "放送回"})
fig.update_traces(line_color="#0c8ea6", textposition="bottom center")
st.plotly_chart(fig, use_container_width=True)

df_plot = df_radio[["date", "hour", "link"]].rename(columns={"date": "放送日付", "hour": "放送時間(h)", "link":"タイトル"}).copy()

fig = go.Figure(
    data=[
        go.Table(
            columnwidth=[1, 1, 5],
            header=dict(
                values=df_plot.columns.to_list()
            ),
            cells=dict(
                values=df_plot.transpose(),
                align=["center", "center", "left"]
            )
        )
    ]
)
st.plotly_chart(fig, use_container_width=True)

# ----------
