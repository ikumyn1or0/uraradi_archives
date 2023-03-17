import streamlit as st
import Visualize as myviz


import setting as mysetting


mysetting.set_site_config()


st.header("📈VISUALIZE RADIO")


st.subheader("放送時間の分布")
myviz.show_histogram_of_length()


st.subheader("時系列での放送時間の推移")
myviz.show_lineplot_of_length()


st.subheader("ゲスト回での放送時間の比較")
myviz.show_violinplot_of_length()
