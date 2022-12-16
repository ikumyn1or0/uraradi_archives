import streamlit as st
import pandas as pd
import glob
import re
import plotly.graph_objects as go

# set page config
st.set_page_config(page_title="裏ラジアーカイブス", page_icon="🦉")

########################
# describe page contents
########################

st.title("📻裏ラジアーカイブス🦉")

# ----------

st.header("テキスト検索")

md_text1 = """
書き起こしたテキストからキーワードを検索することができます。

書き起こしの精度があまり高くないため、キーワードが全て検索結果にヒットするとは限りません。いろいろなキーワードを試すか、テキスト全文表示を活用ください。

「放送回と時間」のリンクに飛ぶことで、その回の再生時間からラジオを再生できます。
"""
st.markdown(md_text1)

# ----------

csv_list = glob.glob("./input/*.csv")
date_list = []
for csv in csv_list:
    date_filename = csv.split("/")[-1]
    date_filename = date_filename.split(".")[0]
    if date_filename != "playlist_裏ラジオウルナイト":
        date_list.append(date_filename)

df_radio = pd.read_csv("./input/playlist_裏ラジオウルナイト.csv")
df_radio["is_transcripted"] = df_radio["date"].apply(lambda date: date in date_list)

def create_yt_link(yt_url, text, time=None):
    yt_link = "https://youtu.be/" + re.search(r"v=(\S)+", yt_url).group()[2:]
    if time is None:
        pass
    else:
        yt_link = yt_link + "?t=" + str(time)
    return f'''<a href="{yt_link}">{text}</a>'''

# ----------

keyword = st.text_input("キーワード", value="",)

# ----------

if st.button('検索'):
    if len(keyword)  <= 0:
        # 検索キーワード長に関するエラー出力
        st.markdown("キーワードは1文字以上でお願いします。")
    else:
        # create empty dataframe object
        df_result = pd.read_csv(f"./input/{date_list[0]}.csv")
        url_c = df_radio[df_radio["date"]==date_list[0]].reset_index(drop=True).loc[0, "url"]
        number_c = df_radio[df_radio["date"]==date_list[0]].reset_index(drop=True).loc[0, "number"]
        df_result["url"] = url_c
        df_result["number"] = number_c
        df_result["date"] = date_list[0]
        df_result = df_result.iloc[0:0].copy()

        # search all radio date
        for date in date_list:
            df_transcripted = pd.read_csv(f"./input/{date}.csv")
            url = df_radio[df_radio["date"]==date].reset_index(drop=True).loc[0, "url"]
            number = df_radio[df_radio["date"]==date].reset_index(drop=True).loc[0, "number"]
            df_transcripted["url"] = url
            df_transcripted["number"] = number
            df_transcripted["date"] = date

            # append search result to dataframe
            df_result = pd.concat([df_result, df_transcripted[df_transcripted['text'].str.contains(str(keyword))].copy()])

        df_result = df_result.reset_index(drop=True)

        if len(df_result) == 0:
            # 検索結果が0拳の際の処理
            st.markdown("一致するキーワードが見つかりませんでした......")
        else:
            # 検索結果の処理
            st.markdown(f"{len(df_result)}件の検索結果が見つかりました。")

            df_result["second"] = df_result["start_h"]*60*60 + df_result["start_m"]*60 + df_result["start_s"]
            df_result["start"] = df_result.apply(lambda df: df["number"] + "-" + str(df["start_h"]).zfill(1) + ":" + str(df["start_m"]).zfill(2) + ":" + str(df["start_s"]).zfill(2), axis=1)
            df_result["link"] = df_result.apply(lambda df: create_yt_link(df["url"], df["start"], df["second"]), axis=1)
            df_result = df_result.sort_values(by=["date", "second"], ascending=[False, True]).reset_index(drop=True)

            df_plot = df_result[["link", "text"]].reset_index().rename(columns={"index": "#", "link": "放送回-再生時間", "text": "テキスト"}).copy()
            df_plot["#"] = df_plot["#"]+1
            st.write(df_plot.to_html(escape=False, index=False), unsafe_allow_html=True)
            # fig = go.Figure(
            #     data=[
            #         go.Table(
            #             columnwidth=[1, 4, 16],
            #             header=dict(
            #                 values=df_plot.columns.to_list()
            #             ),
            #             cells=dict(
            #                 values=df_plot.transpose(),
            #                 align=["center", "center", "left"]
            #             )
            #         )
            #     ]
            # )
            # st.plotly_chart(fig, use_container_width=True)

# ----------
