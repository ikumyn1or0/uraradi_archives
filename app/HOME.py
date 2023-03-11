import streamlit as st
import Visualize as myviz


myviz.set_uraradi_config()


md_text1 = """
本サイトは、774inc.・有閑喫茶あにまーれ所属VTuber[大浦るかこ](https://www.youtube.com/@Rukako_Oura)さんが、金曜日25時から放送中のラジオ「[裏ラジオウルナイト（裏ラジ）](https://youtube.com/playlist?list=PLShwbdwZFm3r77Bwrr1quz2CpqJc6BZVL)」に関する情報をまとめたファンサイトです。

文字起こしAIの[Whisper](https://openai.com/blog/whisper/)によるラジオの書き起こしテキストも利用できます。
"""
st.markdown(md_text1)


st.subheader("各ページの内容")
md_text2 = """
サイドバーから以下のページに飛ぶことができます。（現在のんびりと機能追加中です！）

- **📈VISUALIZE RADIO**: 裏ラジの放送履歴の可視化
- **📃VIEW FULL TEXT**: 書き起こしテキストの全文表示
- **🔍SEARCH TEXT**: 書き起こしテキストのワード検索
- **👀ABOUT**: 裏ラジやWhisper等に関する紹介
"""
st.markdown(md_text2)


st.subheader("過去放送回の一覧")
with st.expander("展開して表示"):
    myviz.show_radios()


st.subheader("更新情報・その他")
md_text3 = """
2023年3月11日現在、#01-#74.5の書き起こしに対応しています。

本サイトにおける「日付」とは、一般的に金曜日の日付を表します。

本サイトに関する質問・バグの報告などは[@mega_ebi](https://twitter.com/mega_ebi)までお願いします。本サイトのソースコードは[こちら](https://github.com/ikumyn1or0/uraradi_archives)。
"""
st.markdown(md_text3)
