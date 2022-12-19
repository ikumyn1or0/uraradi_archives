import streamlit as st
import plotly.express as px
import plotly.colors as pc

import myfunc

st.set_page_config(page_title="裏ラジアーカイブス", page_icon="🦉")

st.title("📻裏ラジアーカイブス🦉")

st.header("裏ラジに関する情報の可視化")

st.subheader("時系列における放送時間の推移")

# ----------
df = myfunc.load_radio_dataset(except_clip=True)
df["hour"] = (df["length_s"]/3600).round(4)

table_columns = {"date": "放送日付", "hour": "放送時間(h)", "number": "放送回"}
df_plot = df[table_columns.keys()].rename(columns=table_columns).copy()

fig = px.line(df_plot, x="放送日付", y="放送時間(h)", text="放送回", markers=True, color_discrete_sequence=[pc.label_rgb(pc.hex_to_rgb("#137D9C"))])
fig.update_traces(textposition="bottom center")
fig.update_layout(margin=dict(t=20, b=0, l=0, r=0))
st.plotly_chart(fig, use_container_width=True)
# ----------

st.subheader("ゲスト回での放送時間の比較")

st.markdown("作成中......")

st.subheader("生データ")

st.caption("なお、放送時間に関する可視化において、総集編は除外しました。")

# ----------
st.dataframe(df_plot, width=400, height=200)
# ----------

