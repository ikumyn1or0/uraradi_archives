import Visualize as myviz
import streamlit as st


myviz.set_uraradi_config()


st.header("🔍SEARCH TEXT")


md_text1 = """
AIによる書き起こしテキストからキーワードを検索することができます。

「再生時間」のリンクに飛ぶことで、その回の再生時間からラジオを再生できます。

固有名詞などの書き起こし精度が低いため、狙ったキーワードが全てヒットするとは限りません。書き起こしテキストの傾向についてはVISUALIZE TEXTやABOUTなどを参考にしてください。
"""
st.markdown(md_text1)


keyword = st.text_input("キーワード", value="")
clicked = st.button("検索", type="primary")
if clicked:
    myviz.show_transcript_search(keyword)
