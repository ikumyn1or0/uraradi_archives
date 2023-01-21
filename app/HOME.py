import streamlit as st

import myvizfunc
import mydatafunc

st.set_page_config(page_title="裏ラジアーカイブス", page_icon="🦉")

st.title("📻裏ラジアーカイブス🦉")

md_text1 = """
このサイトは、774.inc・有閑喫茶あにまーれ所属のVTuber[大浦るかこ](https://www.youtube.com/@Rukako_Oura)さんが金曜日25時から放送中のラジオ[裏ラジオウルナイト（裏ラジ）](https://youtube.com/playlist?list=PLShwbdwZFm3r77Bwrr1quz2CpqJc6BZVL)に関する情報をまとめたファンサイトです。

文字起こしAIの[Whisper](https://openai.com/blog/whisper/)がラジオの音声を書き起こしたテキストデータを利用できます。

サイドバーの各ページからは以下のような機能を利用することができます。（のんびりと機能追加中です！）

- **VISUALIZE RADIO**: 裏ラジのデータを可視化したグラフ
- **VIEW FULL TEXT**: 書き起こしデータの全文表示
- **SEARCH TEXT**: 書き起こしデータのテキスト検索
- **ABOUT**: ラジオ・パーソナリティ・使用したAI技術に関する紹介
"""

st.markdown(md_text1)

st.subheader("過去放送回の一覧")

with st.expander("展開して表示"):
    myvizfunc.show_radio_date_title()

st.subheader("更新情報")

md_text2 = """
2023年1月21日現在、#01-#69の書き起こしに対応しています。

ソースコードは[こちら](https://github.com/ikumyn1or0/uraradi_archives)から。

このサイトに関する質問・バグの報告などは[@mega_ebi](https://twitter.com/mega_ebi)までお願いします。
"""

st.markdown(md_text2)
