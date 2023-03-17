import streamlit as st
import Visualize as myviz


import setting as mysetting


mysetting.set_site_config()


st.header("🔠VISUALIZE TEXT")
st.subheader("ワードクラウドを用いたテキストの可視化")
myviz.show_wordcloud_of_radio()
