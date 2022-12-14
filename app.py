import streamlit as st
import pandas as pd

st.title("裏ラジ アーカイブス🦉")

link1 = "このページは[VTuber大浦るかこ](https://www.youtube.com/@Rukako_Oura)さんが毎週金曜日25時から放送している[裏ラジオウルナイト](https://youtube.com/playlist?list=PLShwbdwZFm3r77Bwrr1quz2CpqJc6BZVL)の放送[書き起こしAI:Whisper](https://whisper.ai/)が書き起こしたものです。"
st.markdown(link1, unsafe_allow_html=True)
st.write("過去回のテキスト検索・放送日時や放送時間の可視化・現在のAI技術のキャッチアップや普及として活用できればと思っています。")
st.write("まだ１回分の書き起こしデータしかないですが、現在のんびりと機能追加中です！")
link2 = "このページに関する質問は[@mega_ebi](https://twitter.com/mega_ebi)までお願いします。"
st.markdown(link2, unsafe_allow_html=True)

df = pd.read_csv("input/2022-11-26.csv")

df["start"] = df["start_h"].apply(lambda x: str(x).zfill(1)) + ":" + \
              df["start_m"].apply(lambda x: str(x).zfill(2)) + ":" + \
              df["start_s"].apply(lambda x: str(x).zfill(2))

st.subheader("2022-11-26放送:【裏ラジ#65】いまどこにいるの、AI")
st.dataframe(df[["start", "text"]], width=800)

