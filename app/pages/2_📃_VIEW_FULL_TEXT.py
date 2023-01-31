import Visualize as myv
import streamlit as st


myv.set_uraradi_page_config()


st.header("📃VIEW FULL TEXT")


md_text1 = """
AIが書き起こしたテキストを全文表示します。

「再生時間」のリンクに飛ぶことで、その回の再生時間からラジオを再生できます。
"""
st.markdown(md_text1)

myv.display_transcript()
