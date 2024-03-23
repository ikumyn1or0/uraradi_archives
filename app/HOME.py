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


with st.expander("大浦るかこさんのななしいんく退社と本サイト運用について(2024年3月23日更新)"):
    md_text3 = """
2024年3月末を以て、大浦るかこさんはななしいんく運営業務から離れることが発表されました。
詳細は[大浦るかこさんのツイート](https://x.com/Rukako_Oura/status/1769651462584537089?s=20)をご確認ください。
同発表では、「これからはみなさんと同じ立場でメンバーを応援」すると記載されており、大浦るかこさんのVTuberとしての活動は終了するものと思われます。

これに伴う本サイトの運用につきまして、サイト公開に使用しているStreamlit Community Cloudが無償使用である限りは**本サイトの公開を継続する**予定です。
ただし、今後様々な事情により予告なく本サイトの公開を終了する場合がありますので、ご了承ください。

また、本サイトの各ページから裏ラジのYouTubeページにアクセスできる機能を実装していましたが、大浦るかこさんのYouTubeが非公開であるためアクセスできない状況となっておりますが、こちらの修正予定はございません。
昨年6月からと変わらず、当該リンクは機能しないことをご承知ください。

本サイトに関しまして疑問点・不明点等ございましたら、[開発者](https://twitter.com/mega_ebi)までご連絡ください。
"""
    st.markdown(md_text3)


with st.expander("更新情報"):
    md_text2 = """
- 2024/03/23:「大浦るかこさんのななしいんく退社と本サイト運用について」を追加
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
