import streamlit as st


import setting as mysetting
import table as mytable


mysetting.set_site_config()


md_text1 = """
本サイトは、ななしいんく所属VTuber[大浦るかこ](https://www.youtube.com/@Rukako_Oura)さんがパーソナリティを務めるラジオ「[裏ラジオウルナイト（裏ラジ）](https://youtube.com/playlist?list=PLShwbdwZFm3r77Bwrr1quz2CpqJc6BZVL)」に関する情報をまとめたファンサイトです。

文字起こしAIの[Whisper](https://openai.com/blog/whisper/)によるラジオの書き起こしテキストも利用できます。

本サイトに記載する情報は全て2023年5月時点のものです。
"""
st.markdown(md_text1)


with st.expander("大浦るかこさんの無期限活動休止と本サイト運用について"):
    md_text3 = """
2023年5月29日をもって大浦るかこさんはタレント活動を無期限活動休止とすることを発表されました。詳細は[ななしいんく公式ツイート](https://twitter.com/774inc_official/status/1662398246508179457?s=20)および[本人ツイート](https://twitter.com/Rukako_Oura/status/1662420079701815297?s=20)を確認ください。

これに伴う本サイトの運用につきましては、[開発者ツイート](https://twitter.com/mega_ebi/status/1667208491742957568?s=20)でお知らせさせていただきました。

2023/6/12のアーカイブ非公開後の本サイトの更新は一旦停止させていただきますが、今後も変わらずこちらのページで後悔を続ける予定となっております。ただし、今後様々な事情により予告なく本サイトの後悔を終了する場合があります。
加えて、本サイトから大浦るかこさんのチャンネルへのリンクが無効となりますので、ご了承ください。

本サイトに関しまして疑問点・不明点等ございましたら、[開発者](https://twitter.com/mega_ebi)までご連絡ください。
"""
    st.markdown(md_text3)


with st.expander("更新情報"):
    md_text2 = """
- 2023/06/25:「大浦るかこさんの無期限活動休止と本サイト運用について」を追加
"""
    st.markdown(md_text2)


st.subheader("各ページの内容")
md_text4 = """
サイドバーから以下のページに飛ぶことができます。

- **📈VISUALIZE RADIO**: 裏ラジの放送履歴の可視化
- **🔠VISUALIZE TEXT**: 書き起こしテキストの可視化
- **📃VIEW FULL TEXT**: 書き起こしテキストとチャットテキストの全文表示
- **🔍SEARCH TEXT**: 書き起こしテキストのワード検索
- **👀ABOUT**: 裏ラジ、Whisper、本サイトに関しての情報
"""
st.markdown(md_text4)


st.subheader("過去放送回の一覧")
mytable.plot_radio()
