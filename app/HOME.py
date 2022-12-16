import streamlit as st
import pandas as pd
import glob

# set page config
st.set_page_config(page_title="裏ラジアーカイブス", page_icon="🦉")

########################
# describe page contents
########################

st.title("📻裏ラジアーカイブス🦉")

# ----------

md_text1 = """
このサイトは、774.inc所属のVTuber[大浦るかこ](https://www.youtube.com/@Rukako_Oura)さんが金曜日25時から放送中のラジオ[裏ラジオウルナイト](https://youtube.com/playlist?list=PLShwbdwZFm3r77Bwrr1quz2CpqJc6BZVL)の過去放送回に関する情報をまとめたサイトです。

文字起こしAIの[Whisper](https://openai.com/blog/whisper/)が裏ラジの音声データを書き起こしたテキストデータを利用できます。

サイドバーの各ページからは以下のような機能を利用することができます。（現在、のんびりと機能追加中です！）
"""
st.markdown(md_text1)

# ----------

md_text2 = """
- **VISUALIZE RADIO**: 過去放送回に関する情報の可視化

- **VIEW FULL TEXT**: 過去放送回の書き起こしデータ全量の表示

- **SEARCH TEXT**: 書き起こしデータを用いたテキストの検索

- **ABOUT**: ラジオ・パーソナリティの紹介や、使用したAI技術に関する詳細

"""
st.markdown(md_text2)

# ----------

st.header("放送済みラジオ回一覧")

st.markdown("現在、総集編を除いた#34-#65の書き起こしに対応しています。")

df_radio = pd.read_csv("./input/playlist_裏ラジオウルナイト.csv")
df_radio["link"] = '<a target="_blank" href='+df_radio["url"]+">"+df_radio["title"]+"</a>"

st.write(df_radio[["date", "link"]].rename(columns={"date": "日付", "link": "タイトル"}).to_html(escape=False, index=False), unsafe_allow_html=True)

# ----------

st.header("更新情報")

md_text2 = """
このサイトに関する質問・バグの報告などは[@mega_ebi](https://twitter.com/mega_ebi)までお願いします。
"""
st.markdown(md_text2)
