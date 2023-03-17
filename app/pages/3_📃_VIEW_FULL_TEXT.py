import streamlit as st


import setting as mysetting
import table as mytable


mysetting.set_site_config()


st.header("📃VIEW FULL TEXT")


md_text1 = """
AIの書き起こしテキストとチャットテキストを全文表示します。

「再生時間」のリンクに飛ぶことで、その回の再生時間からラジオを再生できます。
"""
st.markdown(md_text1)
mytable.plot_transcript_chat()
