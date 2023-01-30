import streamlit as st
import plotly.colors as pc

import myvizfunc
import mydatafunc

OWL_PLOTLY_COLOR_1st = pc.label_rgb(pc.hex_to_rgb("#137D9C"))
OWL_PLOTLY_COLOR_2nd = pc.label_rgb(pc.hex_to_rgb("#13465d"))
OWL_PLOTLY_COLOR_3rd = pc.label_rgb(pc.hex_to_rgb("#b0b210"))

st.set_page_config(page_title="裏ラジアーカイブス", page_icon="🦉")

st.title("📻裏ラジアーカイブス🦉")

st.header("裏ラジに関する情報の可視化")

st.subheader("放送時間の分布")

tab_hist_graph, tab_hist_raw = st.tabs(["グラフ", "生データ"])

myvizfunc.show_histgram_radio_length([tab_hist_graph, tab_hist_raw])

st.subheader("時系列での放送時間の推移")

TIMESERIES_AGG_TYPE = {
    "集計なし": 0,
    "移動平均": 1,
    "月単位": 2,
    "3ヶ月単位": 3,
    "1年単位": 4
}

ts_agg_key = st.selectbox("データを集計したい単位を選択してください。", TIMESERIES_AGG_TYPE.keys())
window = None
if TIMESERIES_AGG_TYPE[ts_agg_key] == 0:
    window = None
elif TIMESERIES_AGG_TYPE[ts_agg_key] == 1:
    window = st.slider("放送時間の移動平均をとる幅を選択してください。", 2, 20)
elif TIMESERIES_AGG_TYPE[ts_agg_key] == 2:
    window = "MS"
elif TIMESERIES_AGG_TYPE[ts_agg_key] == 3:
    window = "QS"
elif TIMESERIES_AGG_TYPE[ts_agg_key] == 4:
    window = "YS"

tab_timeseries_graph, tab_timeseries_raw = st.tabs(["グラフ", "生データ"])

myvizfunc.show_lineplot_radio_length([tab_timeseries_graph, tab_timeseries_raw], window=window)

st.subheader("ゲスト回での放送時間の比較")

GUEST_CLASSIFICATION_TYPE = {
    "ゲストあり回／ゲストなし回を比較": 0,
    "選択したゲスト回／それ以外の回を比較": 1,
    "選択したゲスト回／それ以外のゲスト回／ゲストなし回を比較": 2
}

gu_class_key = st.selectbox("表示したいグラフの種類を選択してください。", GUEST_CLASSIFICATION_TYPE)

_, guest_list = mydatafunc.get_radio_dataset(except_clip=True)
target_guest_list = []
if GUEST_CLASSIFICATION_TYPE[gu_class_key] in [1, 2]:
    target_guest_list = st.multiselect("ゲストを選択してください。", guest_list)

tab_guest_graph, tab_guest_raw = st.tabs(["グラフ", "生データ"])

myvizfunc.show_violinplot_radio_length([tab_guest_graph, tab_guest_raw], GUEST_CLASSIFICATION_TYPE[gu_class_key], target_guest_list)

st.subheader("ワードクラウドを用いた書き起こしテキストの分析")

st.markdown("作成中......")
