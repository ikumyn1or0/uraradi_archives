import streamlit as st
import pandas as pd
import plotly.express as px

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

df_radio = pd.read_csv("./input/playlist_裏ラジオウルナイト.csv")
df_radio["hour"] = df_radio["length"]/3600
df_radio = df_radio[~df_radio["number"].str.contains("総集編")].reset_index(drop=True).copy()
df_radio["caption"] = df_radio["number"].apply(lambda x: x[3:])

df_radio = pd.read_csv("./input/playlist_裏ラジオウルナイト.csv")
df_radio["hour"] = df_radio["length"]/3600
df_radio = df_radio[~df_radio["number"].str.contains("総集編")].reset_index(drop=True).copy()
df_radio["caption"] = df_radio["number"].apply(lambda x: x[3:])

fig = px.line(df_radio, x="date", y="hour", text="caption", markers=True,
              labels={
                  "date": "放送日時",
                  "hour": "放送時間(h)",
                  "caption": "放送回"
              })
fig.update_traces(line_color="#0c8ea6", textposition="bottom center")
st.plotly_chart(fig, use_container_width=True)

st.dataframe(df_radio[["date", "hour", "title"]])

# ----------
