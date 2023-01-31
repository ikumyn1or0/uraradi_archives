import Data as myd
import datetime as dt
import pandas as pd
import plotly.colors as pc
import plotly.express as px
import streamlit as st

PLOTLY_COLOR_THEME = [pc.label_rgb(pc.hex_to_rgb("#137D9C")),
                      pc.label_rgb(pc.hex_to_rgb("#b0b210")),
                      pc.label_rgb(pc.hex_to_rgb("#13465d"))]


def set_uraradi_page_config():
    st.set_page_config(page_title="裏ラジアーカイブス", page_icon="🦉")
    st.title("📻裏ラジアーカイブス🦉")


def display_radio_list() -> None:
    radio = myd.Radio()
    radio.create_html_link_column(display_column="title")
    columns_dict = {"date": "放送日付", "link": "タイトル"}
    df = radio.get_df(columns=columns_dict.keys()).rename(columns=columns_dict)
    st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)


def display_histogram_of_length() -> None:
    radio = myd.Radio(except_clips=True)
    columns_dict = {"number": "放送回", "length_hms": "放送時間(hms)", "length_hour": "放送時間(h)"}
    df = radio.get_df(columns=columns_dict.keys()).rename(columns=columns_dict)

    tab_graph, tab_data = st.tabs(["グラフ", "データ"])
    with tab_graph:
        fig = px.histogram(df,
                           x="放送時間(h)",
                           marginal="rug",
                           hover_name="放送回",
                           hover_data=["放送時間(hms)"],
                           color_discrete_sequence=PLOTLY_COLOR_THEME)
        fig.update_layout(bargap=0.1,
                          margin=dict(t=20, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
    with tab_data:
        st.dataframe(df, use_container_width=True)
        st.download_button(label="CSVデータをダウンロードする",
                           data=df.to_csv(index=False),
                           file_name="dist_of_radio_length.csv",
                           mime="text/csv")
        st.caption("放送時間に関する可視化において、総集編は除外しています。")


def display_lineplot_of_length() -> None:
    AGG_TYPE = {"集計なし": "none",
                "移動平均": "moving",
                "月平均": "month",
                "３ヶ月平均": "quarter",
                "１年平均": "year"}

    agg_key = st.selectbox("データの集計方法を選択してください。", AGG_TYPE.keys())
    agg = AGG_TYPE[agg_key]

    radio = myd.Radio(except_clips=True)
    columns_dict = {"number": "放送回", "date": "放送日付", "length_hms": "放送時間(hms)", "length_hour": "放送時間(h)"}
    df = radio.get_df(columns=columns_dict.keys()).rename(columns=columns_dict)

    if agg == "moving":
        window = st.slider("移動平均の幅を選択してください。", 2, 20)
        df["放送時間(h)"] = df["放送時間(h)"].rolling(window).mean()
        df["放送時間(hms)"] = df["放送時間(h)"].apply(myd.hours_to_hms)
        df["放送回"] = df["放送回"].apply(lambda str: f"{str}から{window}回分の平均")
    elif agg == "month":
        df["datetime"] = pd.to_datetime(df["放送日付"])
        df = df.groupby(pd.Grouper(key="datetime", freq="MS")).mean(numeric_only=True)
        df["放送時間(hms)"] = df["放送時間(h)"].apply(myd.hours_to_hms)
        df["放送日付"] = df.index.astype(str)
        df["放送回"] = df["放送日付"].apply(lambda str: f"{int(str[2:4])}年{int(str[5:7])}月の平均")
    elif agg == "quarter":
        df["datetime"] = pd.to_datetime(df["放送日付"])
        df = df.groupby(pd.Grouper(key="datetime", freq="QS")).mean(numeric_only=True)
        df["放送時間(hms)"] = df["放送時間(h)"].apply(myd.hours_to_hms)
        df["放送日付"] = df.index.astype(str)
        df["放送回"] = df["放送日付"].apply(lambda str: f"{int(str[2:4])}年{int(str[5:7])}月から3ヶ月の平均")
    elif agg == "year":
        df["datetime"] = pd.to_datetime(df["放送日付"])
        df = df.groupby(pd.Grouper(key="datetime", freq="YS")).mean(numeric_only=True)
        df["放送時間(hms)"] = df["放送時間(h)"].apply(myd.hours_to_hms)
        df["放送日付"] = df.index.astype(str)
        df["放送回"] = df["放送日付"].apply(lambda str: f"{int(str[:4])}年の平均")
    df = df[columns_dict.values()]
    df = df.reset_index(drop=True)

    tab_graph, tab_data = st.tabs(["グラフ", "データ"])
    with tab_graph:
        fig = px.line(df,
                      x="放送日付",
                      y="放送時間(h)",
                      markers=True,
                      hover_name="放送回",
                      hover_data=["放送時間(hms)"],
                      color_discrete_sequence=PLOTLY_COLOR_THEME)
        fig.update_traces(textposition="bottom center")
        fig.update_layout(margin=dict(t=20, b=0, l=0, r=0))
        st.plotly_chart(fig)
    with tab_data:
        st.dataframe(df, use_container_width=True)
        st.download_button(label="CSVデータをダウンロードする",
                           data=df.to_csv(index=False),
                           file_name="timeseries_of_radio_length.csv",
                           mime="text/csv")
        st.caption("放送時間に関する可視化において、総集編は除外しています。")


def display_violinplot_of_length_per_guest():
    CLS_TYPE = {
        "ゲストあり回／ゲストなし回を比較": "guest_or_not",
        "選択したゲスト回／それ以外の回を比較": "select_or_not",
        "選択したゲスト回／それ以外のゲスト回／ゲストなし回を比較": "select_or_guest_or_not"}

    cls_key = st.selectbox("比較する方法を選択してください。", CLS_TYPE.keys())
    cls = CLS_TYPE[cls_key]

    radio = myd.Radio(except_clips=True, with_guest_info=True)
    guest_list = radio.get_guests()

    columns_dict = {"number": "放送回", "date": "放送日付", "length_hms": "放送時間(hms)", "length_hour": "放送時間(h)", "class": "分類"}
    df = radio.get_df(columns=columns_dict.keys(), include_guests=True).rename(columns=columns_dict)

    df["with_guest"] = df[guest_list].astype(int).sum(axis=1) > 0
    if cls == "guest_or_not":
        cls_pattern = {
            1: "ゲストあり回",
            0: "ゲストなし回"}
        df["with_guest"] = df[guest_list].astype(int).sum(axis=1) > 0
        df["分類"] = df["with_guest"].astype(int).replace(cls_pattern)
        df.drop("with_guest", axis=1, inplace=True)
    elif cls == "select_or_not":
        cls_pattern = {
            1: "選択したゲスト回",
            0: "それ以外の回"}
        selected_guests = st.multiselect("ゲストを選択してください。", guest_list)
        df["分類"] = df[selected_guests].astype(int).sum(axis=1).clip(lower=0, upper=1)
        df["分類"] = df["分類"].replace(cls_pattern)
    elif cls == "select_or_guest_or_not":
        cls_pattern = {
            2: "選択したゲスト回",
            1: "その他ゲスト回",
            0: "ゲストなし回"}
        selected_guests = st.multiselect("ゲストを選択してください。", guest_list)
        df["分類"] = df["with_guest"].astype(int)
        df["分類"] = df["分類"].mask(df[selected_guests].astype(int).sum(axis=1) > 0, 2)
        df["分類"] = df["分類"].replace(cls_pattern)
        df.drop("with_guest", axis=1, inplace=True)
    df = df[list(columns_dict.values()) + guest_list]
    df = df.reset_index(drop=True)

    tab_graph, tab_data = st.tabs(["グラフ", "データ"])
    with tab_graph:
        fig = px.violin(df,
                        y="放送時間(h)",
                        color="分類",
                        box=True,
                        points="all",
                        hover_name="放送回",
                        hover_data=["放送時間(hms)"],
                        color_discrete_sequence=PLOTLY_COLOR_THEME)
        fig.update_traces(jitter=0.2)
        fig.update_layout(legend=dict(x=0.0, y=1.1),
                          margin=dict(t=20, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
    with tab_data:
        st.dataframe(df, use_container_width=True)
        st.download_button(label="CSVデータをダウンロードする",
                           data=df.to_csv(index=False),
                           file_name="guest_and_radio_length.csv",
                           mime="text/csv")
        st.caption("放送時間に関する可視化において、総集編は除外しています。")


def display_transcript():
    radio = myd.Radio(except_untranscripted_date=True)
    radio_dict = dict(zip(radio.get_df(columns=["title"]).squeeze(), radio.get_df(columns=["date"]).squeeze()))
    selected_title = st.selectbox("表示したい放送回を選択してください。", radio_dict.keys())
    selected_date = radio_dict[selected_title]

    transcript = myd.Transcript(selected_date)
    transcript.create_html_link_column(display_column=None)

    lowerlim_time = dt.time(hour=0, minute=0, second=0)
    upperlim_time = myd.seconds_to_time(transcript.get_length_s())

    selected_range_time = st.slider("表示する再生時間を絞り込むことができます。", value=(lowerlim_time, upperlim_time), min_value=lowerlim_time, max_value=upperlim_time, step=dt.timedelta(minutes=1), format="H:mm:SS")
    selected_range_s = (myd.time_to_seconds(selected_range_time[0]),
                        myd.time_to_seconds(selected_range_time[1]))

    columns_dict = {"link": "再生時間", "text": "テキスト"}
    df = transcript.get_df(columns=columns_dict.keys(), second_range=selected_range_s).rename(columns=columns_dict)
    st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)


def display_text_search_result(keyword: str = "") -> None:
    if len(keyword) <= 0:
        st.markdown("１文字以上のキーワードを入力してください。")
        return
    date_list = myd.get_transcript_date()
    transcript_list = []
    columns_dict = {"link": "再生時間", "text": "テキスト", "date": "日付", "start_s": "再生時刻", "number": "放送回"}
    result_df = pd.DataFrame([], columns=columns_dict.keys())
    with st.spinner("検索中…"):
        for _, date in enumerate(date_list):
            transcript = myd.Transcript(date)
            transcript.create_html_link_column(display_column="number")
            transcript_list.append(transcript)
            result_df = pd.concat([result_df, transcript.get_df(columns=columns_dict.keys(), keyword=keyword)])
        result_df = result_df.rename(columns=columns_dict).sort_values(["日付", "再生時刻"], ascending=[False, True]).reset_index(drop=True)
        if len(result_df) <= 0:
            st.markdown("一致するキーワードが見つかりませんでした。")
        else:
            st.markdown(f"{len(result_df)}件の結果が見つかりました。")
            with st.expander("放送回ごとのヒット件数"):
                order = result_df[["日付", "放送回"]].sort_values("日付")["放送回"].tolist()
                fig = px.histogram(result_df,
                                   x="放送回",
                                   category_orders={"放送回": order},
                                   height=200,
                                   color_discrete_sequence=PLOTLY_COLOR_THEME)
                fig.update_layout(margin=dict(t=20, b=0, l=0, r=0))
                fig.update_xaxes(tickangle=90)
                st.plotly_chart(fig, use_container_width=True)
            st.write(result_df[["再生時間", "テキスト"]].to_html(escape=False, index=False), unsafe_allow_html=True)
