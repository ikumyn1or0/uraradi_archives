import streamlit as st
import Visualize as myviz


myviz.set_uraradi_config()


st.header("🔠VISUALIZE TEXT")
st.subheader("ワードクラウドを用いたテキストの可視化")
myviz.show_wordcloud_of_radio()
