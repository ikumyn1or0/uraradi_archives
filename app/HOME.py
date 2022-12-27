import streamlit as st

import myfunc

st.set_page_config(page_title="裏ラジアーカイブス", page_icon="🦉")

st.title("📻裏ラジアーカイブス🦉")

md_text1 = """
このサイトは、774.inc所属のVTuber[大浦るかこ](https://www.youtube.com/@Rukako_Oura)さんが金曜日25時から放送中のラジオ[裏ラジオウルナイト（裏ラジ）](https://youtube.com/playlist?list=PLShwbdwZFm3r77Bwrr1quz2CpqJc6BZVL)に関する情報をまとめたサイトです。

文字起こしAIの[Whisper](https://openai.com/blog/whisper/)がラジオの音声を書き起こしたテキストデータを利用できます。

サイドバーの各ページからは以下のような機能を利用することができます。（のんびりと機能追加中です！）

- **VISUALIZE RADIO**: 裏ラジに関する情報の可視化
- **VIEW FULL TEXT**: 書き起こしテキストの全文表示
- **SEARCH TEXT**: 書き起こしデータを用いたテキスト検索
- **ABOUT**: ラジオ・パーソナリティの紹介や、使用したAI技術に関する詳細
"""
st.markdown(md_text1)

st.subheader("過去放送回一覧")

with st.expander("展開して表示"):
    # ----------
    df = myfunc.load_radio_dataset(create_link_html=True, linktext="title")
    table_columns = {"date": "放送日付", "link": "タイトル"}
    df_plot = df[table_columns.keys()].rename(columns=table_columns).copy()

    st.write(df_plot.to_html(escape=False, index=False), unsafe_allow_html=True)
    # ----------

st.subheader("更新情報")

md_text2 = """
2022年12月22日現在、総集編を除いた#01-#65の書き起こしに対応しています。

このサイトに関する質問・バグの報告などは[@mega_ebi](https://twitter.com/mega_ebi)までお願いします。
"""
st.markdown(md_text2)
