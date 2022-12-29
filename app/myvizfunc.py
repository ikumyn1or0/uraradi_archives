from datetime import time, timedelta
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.colors as pc

import mydatafunc

PC_OWL_1st = pc.label_rgb(pc.hex_to_rgb("#137D9C"))
PC_OWL_2nd = pc.label_rgb(pc.hex_to_rgb("#13465d"))
PC_OWL_3rd = pc.label_rgb(pc.hex_to_rgb("#b0b210"))


def show_radio_date_title() -> None:
    df, _ = mydatafunc.get_radio_dataset()
    df["link"] = df.apply(lambda df: mydatafunc.create_youtube_html_link(df["url"], df["title"]), axis=1)
    columns = {"date": "放送日付", "link": "タイトル"}
    df_plot = df[columns.keys()].rename(columns=columns).copy()

    st.write(df_plot.to_html(escape=False, index=False), unsafe_allow_html=True)


def show_histgram_radio_length(tabs) -> None:
    df, _ = mydatafunc.get_radio_dataset(except_clip=True)
    columns = {"date": "放送日付", "hour": "放送時間(h)", "number": "放送回"}
    df_plot = df[columns.keys()].rename(columns=columns).copy()

    with tabs[0]:
        fig = px.histogram(df_plot, x="放送時間(h)", marginal="rug", color_discrete_sequence=[PC_OWL_1st])
        fig.update_layout(margin=dict(t=20, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        st.dataframe(df_plot, use_container_width=True)
        st.caption("放送時間に関する可視化において、総集編は除外しています。")


def show_lineplot_radio_length(tabs, window=None) -> None:
    df, _ = mydatafunc.get_radio_dataset(except_clip=True)

    if type(window) is int:
        df["hour"] = df["hour"].rolling(window).mean()
    elif type(window) is str:
        df["datetime"] = pd.to_datetime(df["date"])
        df = df.groupby(pd.Grouper(key="datetime", freq=window)).mean(numeric_only=True)
        df["date"] = df.index.astype(str)
        df["number"] = df["date"].apply(lambda x: x[2:4]+"年"+x[5:7]+"月～")
        df = df.sort_values(by="date", ascending=False).reset_index(drop=True)

    columns = {"date": "放送日付", "hour": "放送時間(h)", "number": "放送回"}
    df_plot = df[columns.keys()].rename(columns=columns).copy()

    with tabs[0]:
        fig = px.line(df_plot, x="放送日付", y="放送時間(h)", text="放送回", markers=True, color_discrete_sequence=[PC_OWL_1st])
        fig.update_traces(textposition="bottom center")
        fig.update_layout(margin=dict(t=20, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        st.dataframe(df_plot, use_container_width=True)
        st.caption("放送時間に関する可視化において、総集編は除外しています。")


def show_violinplot_radio_length(tabs, guest_class_type, target_guest_list=[]) -> None:
    df, guest_list = mydatafunc.get_radio_dataset(except_clip=True)
    df["with_guest"] = df[guest_list].astype(int).sum(axis=1) > 0
    if guest_class_type == 0 or (guest_class_type in [1, 2] and len(target_guest_list) in [0, len(guest_list)]):
        guest_class = {
            1 : "ゲストあり回",
            0 : "ゲストなし回"
        }
        df["class"] = df["with_guest"].astype(int).replace(guest_class)
    elif guest_class_type == 1:
        guest_class = {
            1 : "選択したゲスト回",
            0 : "それ以外の回"
        }
        df["class"] = df[target_guest_list].astype(int).sum(axis=1).clip(lower=0, upper=1)
        df["class"] = df["class"].replace(guest_class)
    elif guest_class_type == 2:
        guest_class = {
            2 : "選択したゲスト回",
            1 : "その他ゲスト回",
            0 : "ゲストなし回"
        }
        df["class"] = df["with_guest"].astype(int)
        df["class"] = df["class"].mask(df[target_guest_list].astype(int).sum(axis=1) > 0, 2)
        df["class"] = df["class"].replace(guest_class)

    columns = {"date": "放送日付", "hour": "放送時間(h)", "number": "放送回", "class": "分類"}
    df_plot = df[list(columns.keys()) + guest_list].rename(columns=columns).copy()

    color_list = [PC_OWL_1st, PC_OWL_2nd, PC_OWL_3rd]

    with tabs[0]:
        fig = px.violin(df_plot, y="放送時間(h)", x="分類", color="分類", box=True, points="all", color_discrete_sequence=color_list)
        fig.update_traces(jitter=0.05)
        fig.update_layout(legend=dict(x=0.01, y=1.1),
                          margin=dict(t=20, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        st.dataframe(df_plot)
        st.caption("放送時間に関する可視化において、総集編は除外しています。")


def select_and_show_full_transcript() -> None:
    df, _ = mydatafunc.get_radio_dataset()

    target_title = st.selectbox("表示したい過去回を選択してください。", df["title"])
    target_index = (df["title"].values == target_title).argmax()


    if df.loc[target_index, "is_transcripted"]:
        target_date = df.loc[target_index, "date"]
        target_url = df.loc[target_index, "url"]

        df_transcripted = mydatafunc.get_transcript_dataset(target_date)
        target_length = df.loc[target_index, "length_s"]
        timemin = time(minute=0, second=0)
        timemax = time(hour=int(target_length/3600), minute=int((target_length%3600)/60)+1, second=0)
        timerange = st.slider("表示する再生時間を指定できます。", value=(timemin, timemax), min_value=timemin, max_value=timemax, step=timedelta(minutes=1), format="H:mm:SS")

        min_s = timerange[0].hour*3600 + timerange[0].minute*60 + timerange[0].second
        max_s = timerange[1].hour*3600 + timerange[1].minute*60 + timerange[1].second

        df_transcripted = df_transcripted[(df_transcripted["start_s"] >= min_s) & (df_transcripted["end_s"] <= max_s)]

        df_transcripted["link"] = df_transcripted.apply(lambda df: mydatafunc.create_youtube_html_link(target_url, link_text=df["start_hms"], time=df["start_s"]), axis=1)
        df_transcripted = df_transcripted.sort_values(by="start_s", ascending=True).reset_index(drop=True)

        table_columns = {"link": "再生時間", "text": "テキスト"}

        df_plot = df_transcripted[table_columns.keys()].rename(columns=table_columns).copy()
        st.write(df_plot.to_html(escape=False, index=False), unsafe_allow_html=True)

    else:
        st.markdown("まだ書き起こしテキストを追加できていない回です。")


def search_and_show_transcript(keyword) -> None:
    date_list = mydatafunc.get_transcript_list()
    df_radio, _ = mydatafunc.get_radio_dataset()

    if len(keyword)  <= 0:
        st.markdown("キーワードは1文字以上でお願いします。")
    else:
        temp_date = date_list[0]
        temp_index_radio = (df_radio["date"].values == temp_date).argmax()
        temp_url = df_radio.loc[temp_index_radio, "url"]
        temp_number = df_radio.loc[temp_index_radio, "number"]

        df_result = mydatafunc.get_transcript_dataset(temp_date)
        df_result["url"] = temp_url
        df_result["number"] = temp_number
        df_result["date"] = temp_date
        df_result = df_result.iloc[0:0].copy()

        for date in date_list:
            df_transcripted = mydatafunc.get_transcript_dataset(date)
            index_radio = (df_radio["date"].values == date).argmax()
            url = df_radio.loc[index_radio, "url"]
            number = df_radio.loc[index_radio, "number"]
            df_transcripted["url"] = url
            df_transcripted["number"] = number
            df_transcripted["date"] = date
            df_result_date = df_transcripted[df_transcripted['text'].str.contains(str(keyword))]

            df_result = pd.concat([df_result, df_result_date.copy()])

        df_result = df_result.reset_index(drop=True)

        if len(df_result) == 0:
            st.markdown("一致するキーワードが見つかりませんでした。")
        else:
            st.markdown(f"{len(df_result)}件の検索結果が見つかりました。")

            df_result["linktext"] = df_result["number"] + " " + df_result["start_hms"]
            df_result["link"] = df_result.apply(lambda df: mydatafunc.create_youtube_html_link(df["url"], link_text=df["linktext"], time=df["start_s"]), axis=1)

            df_result = df_result.sort_values(by=["date", "start_s"], ascending=[False, 
            True]).reset_index(drop=True)
            df_result = df_result.reset_index()
            df_result["index"] = df_result["index"] + 1

            table_columns = {"index": "#", "link": "放送回 再生時間", "text": "テキスト"}

            df_plot = df_result[table_columns.keys()].rename(columns=table_columns).copy()
            fig = px.histogram(df_result, x="number", category_orders=dict(number=df_result["number"].unique().tolist()[::-1]), labels={"number": "放送回"}, height=200, color_discrete_sequence=[pc.label_rgb(pc.hex_to_rgb("#137D9C"))])
            fig.update_layout(margin=dict(t=20, b=0, l=0, r=0))
            fig.update_xaxes(tickangle=90)
            st.plotly_chart(fig, use_container_width=True)

            st.write(df_plot.to_html(escape=False, index=False), unsafe_allow_html=True)

# ----------
