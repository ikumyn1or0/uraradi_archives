import streamlit as st
import pandas as pd
import glob
import re


# load dataset

csv_list = glob.glob("./input/*.csv")
date_list = []
for csv in csv_list:
    date_filename = csv.split("/")[-1]
    date_filename = date_filename.split(".")[0]
    if date_filename != "playlist_裏ラジオウルナイト":
        date_list.append(date_filename)

df_radio = pd.read_csv("./input/playlist_裏ラジオウルナイト.csv")
df_radio["is_transcripted"] = df_radio["date"].apply(lambda date: date in date_list)

# set page config

st.set_page_config(page_title="裏ラジアーカイブス", page_icon="🦉")

# describe page contents

st.title("📻裏ラジアーカイブス🦉")

st.header("テキスト検索")

md_text1 = """
書き起こしたテキストからキーワードを検索することができます。

書き起こしの精度があまり高くないため、狙ったキーワードが全て検索結果にヒットするとは限りません。いろいろなキーワードで試すか、テキスト全文表示を活用ください。

「放送回と時間」のリンクに飛ぶことで、その回の再生時間からラジオを再生できます。
"""
st.markdown(md_text1)

keyword = st.text_input("キーワード", value="",)
if st.button('検索'):
    if len(keyword)  <= 1:
        st.markdown("keyword length is too short")
    else:
        df_result = pd.read_csv(f"./input/{date_list[0]}.csv")
        url_c = df_radio[df_radio["date"]==date_list[0]].reset_index(drop=True).loc[0, "url"]
        number_c = df_radio[df_radio["date"]==date_list[0]].reset_index(drop=True).loc[0, "number"]
        df_result["url"] = url_c
        df_result["number"] = number_c
        df_result["date"] = date_list[0]
        df_result = df_result.iloc[0:0].copy()
        for date in date_list:
            df_transcripted = pd.read_csv(f"./input/{date}.csv")
            url = df_radio[df_radio["date"]==date].reset_index(drop=True).loc[0, "url"]
            number = df_radio[df_radio["date"]==date].reset_index(drop=True).loc[0, "number"]
            df_transcripted["url"] = url
            df_transcripted["number"] = number
            df_transcripted["date"] = date
            df_result = pd.concat([df_result, df_transcripted[df_transcripted['text'].str.contains(str(keyword))]])
        df_result = df_result.reset_index(drop=True)

        df_result["url_id"] = df_result["url"].apply(lambda url: re.search(r"v=(\S)+", url).group()[2:])
        df_result["second"] = df_result["start_h"]*60*60 + df_result["start_m"]*60 + df_result["start_s"]
        df_result["start"] = df_result["start_h"].apply(lambda x: str(x).zfill(1)) + ":" + df_result["start_m"].apply(lambda x: str(x).zfill(2)) + ":" + df_result["start_s"].apply(lambda x: str(x).zfill(2))
        df_result["link"] = '<a target="_blank" href=https://youtu.be/'+df_result["url_id"]+"?t="+df_result["second"].astype(str)+">"+df_result["number"]+" "+df_result["start"]+"</a>"
        df_result = df_result.sort_values(by=["date", "second"], ascending=[False, True])
        st.write(df_result[["link", "text"]].rename(columns={"link": "放送回と時間", "text": "書き起こしテキスト"}).to_html(escape=False, index=False), unsafe_allow_html=True)
