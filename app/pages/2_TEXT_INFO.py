import streamlit as st
import pandas as pd

# load dataset

df = pd.read_csv("./input/2022-11-26.csv")

# set page config

st.set_page_config(page_title="裏ラジアーカイブス", page_icon="🦉")

# describe page contents

st.title("📻裏ラジアーカイブス🦉")

st.header("テキスト検索")

keyword = st.text_input("キーワード", value="",)
if st.button('検索'):
    ret = df[df['text'].str.contains(str(keyword))]
    st.write(ret)
