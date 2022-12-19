import streamlit as st

import myfunc

st.set_page_config(page_title="裏ラジアーカイブス", page_icon="🦉")

st.title("📻裏ラジアーカイブス🦉")

st.header("書き起こしテキスト全文表示")

md_text1 = """
AIによって書き起こしたテキストを全文表示します。

「再生時間」のリンクに飛ぶことで、その回の再生時間からラジオを再生できます。
"""
st.markdown(md_text1)

# ----------
df_radio = myfunc.load_radio_dataset(create_bool_transcripted=True)

target_title = st.selectbox("表示したい過去回を選択してください。", df_radio["title"])
target_index = (df_radio["title"].values == target_title).argmax()
if df_radio.loc[target_index, "is_transcripted"]:
    target_date = df_radio.loc[target_index, "date"]
    url = df_radio.loc[target_index, "url"]

    df_transcripted = myfunc.load_transcripted_dataset(target_date, create_hms=True)
    df_transcripted["link"] = df_transcripted.apply(lambda df: myfunc.create_youtube_link_html(url, linktext=df["start_hms"], time=df["start_s"]), axis=1)
    df_transcripted = df_transcripted.sort_values(by="start_s", ascending=True).reset_index(drop=True)

    table_columns = {"link": "再生時間", "text": "テキスト"}

    df_plot = df_transcripted[table_columns.keys()].rename(columns=table_columns).copy()
    st.write(df_plot.to_html(escape=False, index=False), unsafe_allow_html=True)

else:
    st.markdown("まだ書き起こしテキストを追加できていない回です。")
# ----------
