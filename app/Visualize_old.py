import Data_old as myd
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
