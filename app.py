import streamlit as st
import pandas as pd

st.title("裏ラジ アーカイブス🦉")

link = "このページは[VTuber大浦るかこ](https://www.youtube.com/@Rukako_Oura)さんが毎週金曜日25時から放送している[裏ラジオウルナイト](https://youtube.com/playlist?list=PLShwbdwZFm3r77Bwrr1quz2CpqJc6BZVL)の放送内容を記録したものです。"
st.markdown(link, unsafe_allow_html=True)

st.write("現在鋭意作成中！")

df = pd.read_csv("input/2022-05-06.csv")

df["start"] = df["start_h"].apply(lambda x: str(x).zfill(1)) + ":" + \
              df["start_m"].apply(lambda x: str(x).zfill(2)) + ":" + \
              df["start_s"].apply(lambda x: str(x).zfill(2))

st.subheader("2022-05-06放送回")
st.dataframe(df[["start", "text"]], width=600)

st.write("created by meba_ebi")
