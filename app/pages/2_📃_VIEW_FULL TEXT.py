import streamlit as st

import myvizfunc
import mydatafunc

st.set_page_config(page_title="裏ラジアーカイブス", page_icon="🦉")

st.title("📻裏ラジアーカイブス🦉")

st.header("書き起こしテキスト全文表示")

md_text1 = """
AIが書き起こしたテキストを全文表示します。

「再生時間」のリンクに飛ぶことで、その回の再生時間からラジオを再生できます。

スライドバーを使うことで、再生時間を絞り込むことができます。
"""
st.markdown(md_text1)

myvizfunc.select_and_show_full_transcript()
# ----------
