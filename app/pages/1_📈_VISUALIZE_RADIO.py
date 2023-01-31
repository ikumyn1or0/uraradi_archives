import Visualize as myv
import streamlit as st


myv.set_uraradi_page_config()


st.header("📈VISUALIZE RADIO")


st.subheader("放送時間の分布")

myv.display_histogram_of_length()


st.subheader("時系列での放送時間の推移")

myv.display_lineplot_of_length()


st.subheader("ゲスト回での放送時間の比較")

myv.display_violinplot_of_length_per_guest()


st.subheader("ワードクラウドを用いた書き起こしテキストの分析")

st.markdown("作成中......")
