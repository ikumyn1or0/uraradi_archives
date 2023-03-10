import Data as mydata
import datetime
import pandas as pd
import plotly.colors as pc
import plotly.express as px
import streamlit as st


PLOTLY_COLOR_THEME = [pc.label_rgb(pc.hex_to_rgb("#137D9C")),
                      pc.label_rgb(pc.hex_to_rgb("#b0b210")),
                      pc.label_rgb(pc.hex_to_rgb("#13465d"))]


def set_uraradi_config():
    st.set_page_config(page_title="裏ラジアーカイブス", page_icon="🦉")
    st.title("📻裏ラジアーカイブス🦉")


def load_RadioList_from_sessionstate():
    if "radiolist" not in st.session_state:
        st.session_state.radiolist = mydata.RadioList()
        print("radiolist loaded.")
    return st.session_state.radiolist


def load_TranscriptList_from_sessionstate():
    if "transcriptlist" not in st.session_state:
        st.session_state.transcriptlist = mydata.TranscriptList()
        print("transcriptlist loaded.")
    return st.session_state.transcriptlist


def show_tabs_for_graph_and_data():
    return st.tabs(["グラフ", "データ"])


def show_download_button(df, file_name):
    st.download_button(label="CSVデータをダウンロードする",
                       data=df.to_csv(index=False),
                       file_name=file_name,
                       mime="text/csv")


def show_radios():
    radiolist = load_RadioList_from_sessionstate()
    table = []
    table_column = ["放送日付",
                    "タイトル"]
    for radioinfo in radiolist.RadioInfos:
        row = [radioinfo.date,
               mydata.create_html_link(radioinfo.get_youtube_url(), radioinfo.title)]
        table.append(row)
    df = pd.DataFrame(table, columns=table_column)
    df = df.sort_values(by="放送日付", ascending=False).reset_index(drop=True)
    st.write(df.to_html(escape=False,
                        index=False,
                        col_space={"放送日付": '110px'},
                        justify="center"),
             unsafe_allow_html=True)


def show_histogram_of_length():
    radiolist = load_RadioList_from_sessionstate()
    table = []
    table_column = ["放送日付",
                    "放送回",
                    "放送時間(hms)",
                    "放送時間(h)",
                    "放送時間(s)"]
    for radioinfo in radiolist.RadioInfos:
        if radioinfo.is_clip:
            continue
        row = [radioinfo.date,
               radioinfo.get_shorten_title(),
               radioinfo.get_length_hms(),
               radioinfo.get_length_hour(),
               radioinfo.length_s]
        table.append(row)
    df = pd.DataFrame(table, columns=table_column)
    df = df.sort_values(by="放送日付", ascending=False).reset_index(drop=True)
    df = df.drop("放送日付", axis=1)

    tab_graph, tab_data = show_tabs_for_graph_and_data()

    with tab_graph:
        fig = px.histogram(df,
                           x="放送時間(h)",
                           marginal="rug",
                           hover_name="放送回",
                           hover_data=["放送時間(hms)"],
                           color_discrete_sequence=PLOTLY_COLOR_THEME)
        fig.update_layout(margin=dict(t=20,
                                      b=0,
                                      l=0,
                                      r=0))
        st.plotly_chart(fig, use_container_width=True)

    with tab_data:
        st.markdown("放送時間に関する可視化において、総集編は除外しています。")
        st.dataframe(df, use_container_width=True)
        show_download_button(df, "distribution_of_length.csv")


def show_lineplot_of_length():
    radiolist = load_RadioList_from_sessionstate()
    table = []
    table_column = ["放送日付",
                    "放送回",
                    "放送時間(hms)",
                    "放送時間(h)",
                    "放送時間(s)"]
    for radioinfo in radiolist.RadioInfos:
        if radioinfo.is_clip:
            continue
        row = [radioinfo.date,
               radioinfo.get_shorten_title(),
               radioinfo.get_length_hms(),
               radioinfo.get_length_hour(),
               radioinfo.length_s]
        table.append(row)
    df = pd.DataFrame(table, columns=table_column)

    LINEPLOT_AGG_STYLE = {"集計なし": 0,
                          "移動平均": 1,
                          "月平均": 2,
                          "３ヶ月平均": 3,
                          "１年平均": 4}
    agg_key = st.selectbox("データの集計方法を選択してください。", LINEPLOT_AGG_STYLE.keys())
    agg = LINEPLOT_AGG_STYLE[agg_key]
    if agg == 1:    # 移動平均
        window = st.slider("移動平均をとる幅を選択してください。", 2, 20)
        df["放送時間(s)"] = df["放送時間(s)"].rolling(window, min_periods=1).mean().round().astype(int)
        df["放送時間(h)"] = df["放送時間(s)"].apply(mydata.from_seconds_to_hour)
        df["放送時間(hms)"] = df["放送時間(s)"].apply(mydata.from_seconds_to_hms_format)
        df["放送回"] = df["放送回"].apply(lambda str: f"{str}から最大{window}回の平均")
    elif agg == 2:  # 月平均
        df["datetime"] = pd.to_datetime(df["放送日付"])
        df = df.groupby(pd.Grouper(key="datetime", freq="MS")).mean(numeric_only=True)
        df["放送時間(s)"] = df["放送時間(s)"].round().astype(int)
        df["放送時間(h)"] = df["放送時間(s)"].apply(mydata.from_seconds_to_hour)
        df["放送時間(hms)"] = df["放送時間(s)"].apply(mydata.from_seconds_to_hms_format)
        df["放送日付"] = df.index.astype(str)
        df["放送回"] = df["放送日付"].apply(lambda str: f"{int(str[2:4])}年{int(str[5:7])}月の平均")
    elif agg == 3:  # ３ヶ月平均
        df["datetime"] = pd.to_datetime(df["放送日付"])
        df = df.groupby(pd.Grouper(key="datetime", freq="QS")).mean(numeric_only=True)
        df["放送時間(s)"] = df["放送時間(s)"].round().astype(int)
        df["放送時間(h)"] = df["放送時間(s)"].apply(mydata.from_seconds_to_hour)
        df["放送時間(hms)"] = df["放送時間(s)"].apply(mydata.from_seconds_to_hms_format)
        df["放送日付"] = df.index.astype(str)
        df["放送回"] = df["放送日付"].apply(lambda str: f"{int(str[2:4])}年{int(str[5:7])}月から3ヶ月の平均")
    elif agg == 4:  # １年平均
        df["datetime"] = pd.to_datetime(df["放送日付"])
        df = df.groupby(pd.Grouper(key="datetime", freq="YS")).mean(numeric_only=True)
        df["放送時間(s)"] = df["放送時間(s)"].round().astype(int)
        df["放送時間(h)"] = df["放送時間(s)"].apply(mydata.from_seconds_to_hour)
        df["放送時間(hms)"] = df["放送時間(s)"].apply(mydata.from_seconds_to_hms_format)
        df["放送日付"] = df.index.astype(str)
        df["放送回"] = df["放送日付"].apply(lambda str: f"{int(str[:4])}年の平均")
    df = df[table_column]
    df = df.sort_values(by="放送日付", ascending=False).reset_index(drop=True)

    tab_graph, tab_data = show_tabs_for_graph_and_data()

    with tab_graph:
        fig = px.line(df,
                      x="放送日付",
                      y="放送時間(h)",
                      markers=True,
                      hover_name="放送回",
                      hover_data=["放送時間(hms)"],
                      color_discrete_sequence=PLOTLY_COLOR_THEME)
        fig.update_traces(textposition="bottom center")
        fig.update_layout(margin=dict(t=20,
                                      b=0,
                                      l=0,
                                      r=0))
        st.plotly_chart(fig, use_container_width=True)

    with tab_data:
        st.markdown("放送時間に関する可視化において、総集編は除外しています。")
        st.dataframe(df, use_container_width=True)
        show_download_button(df, "timeseries_and_length.csv")


def show_violinplot_of_length():
    radiolist = load_RadioList_from_sessionstate()

    VIOLONPLOT_CLS_STYLE = {"ゲストあり回／ゲストなし回を比較": 0,
                            "選択したゲスト回／それ以外の回を比較": 1,
                            "選択したゲスト回／それ以外のゲスト回／ゲストなし回を比較": 2}
    agg_key = st.selectbox("比較する方法を選択してください。", VIOLONPLOT_CLS_STYLE.keys())
    agg = VIOLONPLOT_CLS_STYLE[agg_key]
    selected_guests = []
    if agg != 0:    # 移動平均
        selected_guests = st.multiselect("ゲストを選択してください。", radiolist.get_guest_list())

    table = []
    table_column = ["放送日付",
                    "放送回",
                    "放送時間(hms)",
                    "放送時間(h)",
                    "放送時間(s)",
                    "分類"]
    for radioinfo in radiolist.RadioInfos:
        if radioinfo.is_clip:
            continue
        guest_class = "未定義"
        if agg == 0:
            if len(radioinfo.guests) == 0:
                guest_class = "ゲストなし回"
            else:
                guest_class = "ゲストあり回"
        if agg == 1:
            if len(set(selected_guests) & set(radioinfo.guests)) > 0:
                guest_class = "選択したゲスト回"
            else:
                guest_class = "それ以外の回"
        if agg == 2:
            if len(radioinfo.guests) == 0:
                guest_class = "ゲストなし回"
            elif len(set(selected_guests) & set(radioinfo.guests)) > 0:
                guest_class = "選択したゲスト回"
            else:
                guest_class = "その他ゲスト回"
        row = [radioinfo.date,
               radioinfo.get_shorten_title(),
               radioinfo.get_length_hms(),
               radioinfo.get_length_hour(),
               radioinfo.length_s,
               guest_class]
        table.append(row)
    df = pd.DataFrame(table, columns=table_column)

    tab_graph, tab_data = show_tabs_for_graph_and_data()

    with tab_graph:
        fig = px.violin(df,
                        x="分類",
                        y="放送時間(h)",
                        color="分類",
                        box=True,
                        points="all",
                        hover_name="放送回",
                        hover_data=["放送時間(hms)"],
                        color_discrete_sequence=PLOTLY_COLOR_THEME)
        fig.update_traces(jitter=0.3)
        fig.update_layout(showlegend=False,
                          margin=dict(t=20, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    with tab_data:
        st.markdown("放送時間に関する可視化において、総集編は除外しています。")
        st.dataframe(df, use_container_width=True)
        show_download_button(df, "guest_and_length.csv")


def show_full_transcript():
    radiolist = load_RadioList_from_sessionstate()
    transcriptlist = load_TranscriptList_from_sessionstate()

    radio_dict = {}
    for radioinfo in radiolist.RadioInfos:
        radio_dict[radioinfo.title] = radioinfo.date
    selected_title = st.selectbox("表示したい放送回を選択してください。", radio_dict.keys())
    selected_date = radio_dict[selected_title]
    selected_radio = radiolist.get_radioinfo_in(selected_date)
    selected_transcript = transcriptlist.get_transcript_in(selected_date)
    # st.write(selected_transcript)

    if selected_transcript is None:
        st.markdown("書き起こしを追加できていません。")
    else:
        lowerrange_t = datetime.time(hour=0, minute=0, second=0)
        upperrange_t = mydata.from_seconds_to_time(selected_radio.length_s)
        selected_range_t = st.slider("表示する再生時間を絞り込むことができます。",
                                     value=(lowerrange_t, upperrange_t),
                                     min_value=lowerrange_t,
                                     max_value=upperrange_t,
                                     step=datetime.timedelta(minutes=1),
                                     format="H:mm:SS")
        lowerrange_s = mydata.from_time_to_seconds(selected_range_t[0])
        upperrange_s = mydata.from_time_to_seconds(selected_range_t[1])

        table = []
        table_column = ["start_s",
                        "再生時間",
                        "テキスト"]
        for text in selected_transcript.texts:
            if lowerrange_s <= text.start_s and text.end_s <= upperrange_s:
                row = [text.start_s,
                       mydata.create_html_link(selected_radio.get_youtube_url(second=text.start_s),
                                               mydata.from_seconds_to_hms_format(text.start_s)),
                       text.text]
                table.append(row)
        df = pd.DataFrame(table, columns=table_column)
        df = df.sort_values(by="start_s", ascending=True).reset_index(drop=True)
        df = df.drop("start_s", axis=1)
        st.write(df.to_html(escape=False,
                            index=False,
                            col_space={"再生時間": '110px'},
                            justify="center"),
                 unsafe_allow_html=True)


def show_transcript_search(keyword):
    radiolist = load_RadioList_from_sessionstate()
    transcriptlist = load_TranscriptList_from_sessionstate()
    table = []
    table_column = ["date",
                    "start_s",
                    "title",
                    "再生時間",
                    "テキスト"]
    for transcript in transcriptlist.Transcripts:
        radioinfo = radiolist.get_radioinfo_in(transcript.date)
        for text in transcript.texts:
            if keyword in text.text:
                link = radioinfo.get_shorten_title() + " " + mydata.from_seconds_to_hms_format(text.start_s)
                row = [transcript.date,
                       text.start_s,
                       radioinfo.get_shorten_title(),
                       mydata.create_html_link(radioinfo.get_youtube_url(second=text.start_s),
                                               link),
                       text.text]
                table.append(row)
    df = pd.DataFrame(table, columns=table_column)
    df = df.sort_values(by=["date", "start_s"], ascending=[False, True]).reset_index(drop=True)

    with st.expander("放送回ごとの検索結果"):
        hist_df = df[["date", "title"]].copy()
        hist_df = hist_df.sort_values(by="date").reset_index(drop=True)
        hist_df["title"] = "裏ラジ" + hist_df["title"]
        fig = px.histogram(hist_df,
                           x="title",
                           height=250,
                           color_discrete_sequence=PLOTLY_COLOR_THEME)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"{len(df)}件の結果が見つかりました。")
    df = df.drop(["date", "start_s", "title"], axis=1)
    if len(df) >= 10000:
        st.markdown("検索結果が10000件以上のため、表示項目を制限しています。")
        df = df.head(10000)

    st.write(df.to_html(escape=False,
                        index=False,
                        col_space={"再生時間": '110px'},
                        justify="center"),
             unsafe_allow_html=True)
