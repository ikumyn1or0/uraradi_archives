import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.colors as pc

import myfunc

OWL_PLOTLY_COLOR_1st = pc.label_rgb(pc.hex_to_rgb("#137D9C"))
OWL_PLOTLY_COLOR_2nd = pc.label_rgb(pc.hex_to_rgb("#13465d"))
OWL_PLOTLY_COLOR_3rd = pc.label_rgb(pc.hex_to_rgb("#b0b210"))

st.set_page_config(page_title="裏ラジアーカイブス", page_icon="🦉")

st.title("📻裏ラジアーカイブス🦉")

st.header("裏ラジに関する情報の可視化")

st.subheader("時系列での放送時間の推移")

df_ts = myfunc.load_radio_dataset(except_clip=True, create_hour=True)

RADIO_TS_AGG_TYPE = {
    "週単位(集計なし)": 1,
    "月単位": 2,
    "3ヶ月単位": 3,
    "1年単位": 4,
    "移動平均": 5
    }

by = st.selectbox("データを集計したい単位を選択してください。", RADIO_TS_AGG_TYPE.keys())

if RADIO_TS_AGG_TYPE[by] == 1:
    pass
elif RADIO_TS_AGG_TYPE[by] == 2:
    df_ts = myfunc.aggregate_radio_hour_by_date(df_ts, "MS")
elif RADIO_TS_AGG_TYPE[by] == 3:
    df_ts = myfunc.aggregate_radio_hour_by_date(df_ts, "QS")
elif RADIO_TS_AGG_TYPE[by] == 4:
    df_ts = myfunc.aggregate_radio_hour_by_date(df_ts, "YS")
elif RADIO_TS_AGG_TYPE[by] == 5:
    window = st.slider("移動平均をとる幅を選択してください。", 2, 20)
    df_ts["hour"] = df_ts["hour"].rolling(window, center=True).mean()
else:
    st.error("select boxの値が不正です。")

ts_columns = {"date": "放送日付", "hour": "放送時間(h)", "number": "放送回"}
df_ts_plot = df_ts[ts_columns.keys()].rename(columns=ts_columns).copy()

tab_ts_graph, tab_ts_raw = st.tabs(["グラフ", "生データ"])

with tab_ts_graph:
    fig = px.line(df_ts_plot, x="放送日付", y="放送時間(h)", text="放送回", markers=True, color_discrete_sequence=[OWL_PLOTLY_COLOR_1st])
    fig.update_traces(textposition="bottom center")
    fig.update_layout(margin=dict(t=20, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

with tab_ts_raw:
    st.caption("なお、放送時間に関する可視化において、総集編は除外しています。")
    st.dataframe(df_ts_plot, height=200, use_container_width=True)

st.subheader("ゲスト回での放送時間の比較")

df_gu, guest_list = myfunc.load_radio_dataset(except_clip=True, create_hour=True, add_guest_info=True)
df_gu["exist_guest"] = df_gu[guest_list].astype(int).sum(axis=1).apply(lambda x: True if x > 0 else False)

RADIO_GU_TYPE = {
    "ゲストあり回／ゲストなし回の比較": 1,
    "特定のゲスト回／それ以外の比較": 2,
    "特定のゲスト回／それ以外のゲスト回／ゲストなし回の比較": 3
}

gu_style = st.selectbox("表示したいグラフの種類を選択してください。", RADIO_GU_TYPE)

if RADIO_GU_TYPE[gu_style] == 1:
    group_dict = {
        0 : "ゲストなし",
        1 : "ゲストあり"
    }
    df_gu["group"] = df_gu["exist_guest"].astype(int)
    df_gu["group"] = df_gu["group"].replace(group_dict)
elif RADIO_GU_TYPE[gu_style] == 2:
    group_dict = {
        0 : "その他",
        1 : "選択したゲスト"
    }
    selected_guests = st.multiselect("ゲストを選択してください。", guest_list)
    if len(selected_guests) == 0:
        st.write("ゲストを1人以上選択してください。")
        df_gu["group"] = df_gu["exist_guest"].astype(int)
    elif len(selected_guests) >= len(guest_list):
        st.write("全てのゲストが選択されています。")
        df_gu["group"] = df_gu["exist_guest"].astype(int)
    else:
        df_gu["group"] = df_gu[selected_guests].astype(int).sum(axis=1).apply(lambda x: True if x > 0 else False)
        df_gu["group"] = df_gu["group"].astype(int)
    df_gu["group"] = df_gu["group"].replace(group_dict)
elif RADIO_GU_TYPE[gu_style] == 3:
    group_dict = {
        0 : "ゲストなし",
        1 : "その他ゲスト",
        2 : "選択したゲスト"
    }
    selected_guests = st.multiselect("ゲストを選択してください。", guest_list)
    if len(selected_guests) == 0:
        st.write("ゲストを1人以上選択してください。")
        df_gu["group"] = df_gu["exist_guest"]
    elif len(selected_guests) >= len(guest_list):
        st.write("全てのゲストが選択されています。")
        df_gu["group"] = df_gu["exist_guest"]
    else:
        df_gu["exist_selected_guest"] = df_gu[selected_guests].astype(int).sum(axis=1).apply(lambda x: True if x > 0 else False)
        df_gu["group"] = df_gu["exist_selected_guest"]*1 + df_gu["exist_guest"]*1
    df_gu["group"] = df_gu["group"].replace(group_dict)
else:
    st.error("select boxの値が不正です。")

gu_columns = {"date": "放送日付", "hour": "放送時間(h)", "group": "区分"}
df_gu_plot = df_gu[list(gu_columns.keys())].rename(columns=gu_columns).copy()

df_gu_raw = df_gu[list(gu_columns.keys()) + guest_list].rename(columns=gu_columns).copy()

tab_gu_graph, tab_gu_raw = st.tabs(["グラフ", "生データ"])

with tab_gu_graph:
    df_color_list = []
    if df_gu_plot["区分"].nunique()==2:
        df_color_list = [OWL_PLOTLY_COLOR_1st, OWL_PLOTLY_COLOR_2nd]
    elif df_gu_plot["区分"].nunique()==3:
        df_color_list = [OWL_PLOTLY_COLOR_1st, OWL_PLOTLY_COLOR_2nd, OWL_PLOTLY_COLOR_3rd]
    fig = px.violin(df_gu_plot, y="放送時間(h)", x="区分", color="区分", box=True, points="all", color_discrete_sequence=df_color_list)
    # fig = px.violin(df_gu_plot, y="放送時間(h)", x="区分", color="区分", box=True, points="all")
    fig.update_traces(jitter=0.05)
    st.plotly_chart(fig, use_container_width=True)

with tab_gu_raw:
    st.dataframe(df_gu_raw)
