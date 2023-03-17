import streamlit as st


import setting as mysetting
import table as mytable


mysetting.set_site_config()


md_text1 = """
本サイトは、774inc.・有閑喫茶あにまーれ所属VTuber[大浦るかこ](https://www.youtube.com/@Rukako_Oura)さんが、金曜日25時から放送中のラジオ「[裏ラジオウルナイト（裏ラジ）](https://youtube.com/playlist?list=PLShwbdwZFm3r77Bwrr1quz2CpqJc6BZVL)」に関する情報をまとめたファンサイトです。

文字起こしAIの[Whisper](https://openai.com/blog/whisper/)によるラジオの書き起こしテキストも利用できます。
"""
st.markdown(md_text1)

with st.expander("更新情報"):
    md_text2 = """
- 2023/03/18:チャットコメント全文表示機能を追加しました。
- 2023/03/11:#74.5の書き起こしを追加しました。
- 2023/03/11:ワードクラウド可視化機能を追加しました。
"""
    st.markdown(md_text2)


st.subheader("各ページの内容")
md_text3 = """
サイドバーから以下のページに飛ぶことができます。（現在のんびりと機能追加中です！）

- **📈VISUALIZE RADIO**: 裏ラジの放送履歴の可視化
- **🔠VISUALIZE TEXT**: 書き起こしテキストの可視化
- **📃VIEW FULL TEXT**: 書き起こしテキストとチャットテキストの全文表示
- **🔍SEARCH TEXT**: 書き起こしテキストのワード検索
- **👀ABOUT**: 裏ラジ、Whisper、本サイトに関しての情報
"""
st.markdown(md_text3)


st.subheader("過去放送回の一覧")
mytable.plot_radio()
