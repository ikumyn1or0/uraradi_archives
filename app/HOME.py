import streamlit as st
import pandas as pd
import glob

# load dataset

csv_list = glob.glob("./input/*.csv")
date_list = []
for csv in csv_list:
    date_filename = csv.split("/")[-1]
    date_filename = date_filename.split(".")[0]
    date_list.append(date_filename)

df_radio = pd.read_csv("./input/playlist_裏ラジオウルナイト.csv")
df = df_radio.copy()
df["link"] = '<a target="_blank" href='+df["url"]+">"+df["title"]+"</a>"
df["transcripted"] = df["date"].apply(lambda date: "テキスト有" if date in date_list else "テキスト無")
df = df[["date", "link", "transcripted"]]

# set page config

st.set_page_config(page_title="裏ラジアーカイブス", page_icon="🦉")

# describe page contents

st.title("📻裏ラジアーカイブス🦉")

st.header("このサイトについて")

md_text1 = """
このサイトは、VTuber[大浦るかこ](https://www.youtube.com/@Rukako_Oura)さんが金曜日25時から放送中のラジオ[裏ラジオウルナイト](https://youtube.com/playlist?list=PLShwbdwZFm3r77Bwrr1quz2CpqJc6BZVL)の過去放送回に関する情報をまとめたサイトです。

文字起こしAIの[Whisper](https://openai.com/blog/whisper/)が裏ラジの音声データを書き起こしたテキストデータを利用することもできます。

サイドバーの各ページからは以下のような機能を利用することができます。
"""
st.markdown(md_text1)

st.warning("現在、のんびりと機能追加中です！")

md_text2 = """
**RADIO INFO**: 過去放送回に関する情報の検索・可視化

**TEXT INFO**: 書き起こしデータを用いたテキスト検索・可視化

**ABOUT**: ラジオやパーソナリティの紹介や、このページで使用したAI技術に関する詳細

"""
st.markdown(md_text2)

st.header("放送済みラジオ回一覧")

st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)

st.header("更新情報")

md_text2 = """
このページに関する質問は[@mega_ebi](https://twitter.com/mega_ebi)までお願いします。
"""
st.markdown(md_text2)
