import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.colors as pc

import myvizfunc
import mydatafunc

st.set_page_config(page_title="裏ラジアーカイブス", page_icon="🦉")

st.title("📻裏ラジアーカイブス🦉")

st.header("テキスト検索")

md_text1 = """
AIが書き起こしたテキストからキーワードを検索することができます。

「放送回 再生時間」のリンクに飛ぶことで、その回の再生時間からラジオを再生できます。

書き起こしの精度が高くないため、狙ったキーワードが全てヒットするとは限りません。書き起こしテキストの傾向もご参考ください。
"""
st.markdown(md_text1)

with st.expander("書き起こしテキストの傾向"):
    md_text2 = """
    - 「大浦るかこ」「あにまーれ」などの人名や固有名詞は、認識精度が低いか、原文とは異なる表記で認識されていることが多いです。
    - 一般用語ではない単語は、ひらがなやカタカナのみで表記されていることが多いです。
    - 固有名詞以外の文章は認識精度が高いです。
    - ラジオ冒頭・最後のBGMがノイズとして影響され、本来発話していない部分でも何かしら発話していると誤認識されていることがあります。
    - 全文検索を眺めてみることで、より詳しい書き起こしテキストの傾向が理解できると思います。
"""
    st.markdown(md_text2)

keyword = st.text_input("キーワード", value="",)

clicked = st.button("検索", type="primary")

if clicked:
    myvizfunc.search_and_show_transcript(keyword)
