import streamlit as st
import Visualize as myv


myv.set_uraradi_page_config()


md_text1 = """
本サイトは、774.inc・有閑喫茶あにまーれ所属VTuber[大浦るかこ](https://www.youtube.com/@Rukako_Oura)さんが、金曜日25時から放送中のラジオ「[裏ラジオウルナイト（裏ラジ）](https://youtube.com/playlist?list=PLShwbdwZFm3r77Bwrr1quz2CpqJc6BZVL)」に関するファンサイトです。

文字起こしAIの[Whisper](https://openai.com/blog/whisper/)によるラジオ音声の書き起こしテキストも利用できます。
"""

st.markdown(md_text1)


st.subheader("各ページの内容")

md_text2 = """
サイドバーから以下のページに飛ぶことができます。（現在のんびりと機能追加中です！）

- **VISUALIZE RADIO**: 裏ラジのデータの可視化
- **VIEW FULL TEXT**: 書き起こしテキストの全文表示
- **SEARCH TEXT**: 書き起こしテキストのテキスト検索
- **ABOUT**: ラジオ・パーソナリティ・使用したAI技術などに関する紹介
"""
st.markdown(md_text2)


st.subheader("過去放送回の一覧")

with st.expander("展開して表示"):
    myv.display_radio_list()


st.subheader("更新情報・その他")

md_text3 = """
2023年2月4日現在、#01-#70の書き起こしに対応しています。

本サイトにおいて「（ラジオが放送される）日付」とは金曜日のことを指します。

本サイトに関する質問・バグの報告などは[@mega_ebi](https://twitter.com/mega_ebi)までお願いします。ソースコードは[こちら](https://github.com/ikumyn1or0/uraradi_archives)。
"""

st.markdown(md_text3)
