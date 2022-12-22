import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.colors as pc

import myfunc

st.set_page_config(page_title="裏ラジアーカイブス", page_icon="🦉")

st.title("📻裏ラジアーカイブス🦉")

st.header("テキスト検索")

md_text1 = """
書き起こしたテキストからキーワードを検索することができます。

「放送回 再生時間」のリンクに飛ぶことで、その回の再生時間からラジオを再生できます。

書き起こしの精度が高くないため、狙ったキーワードが全てヒットするとは限りません。書き起こしテキストの傾向もご参考ください。
"""
st.markdown(md_text1)

with st.expander("書き起こしテキストの傾向"):
    md_text2 = """
    - 「大浦るかこ」「あにまーれ」などの人名や固有名詞は、認識精度が低いか、原文とは異なる表記で認識されていることが多いです。
    - 一般用語ではない単語は、ひらがなやカタカナのみで表記されていることが多いです。
    - 固有名詞以外の文章は認識精度が高いです。
    - ラジオ冒頭・最後のBGMがノイズとして影響され、本来発話していない部分でも何かしら発話していると誤認識されていることがあります。
    - 書き起こしテキストの傾向を理解するために、全文検索を活用ください。
    """
    st.markdown(md_text2)

date_list = myfunc.get_transcripted_csv_list()
df_radio = myfunc.load_radio_dataset(create_bool_transcripted=True)

keyword = st.text_input("キーワード", value="",)

clicked = st.button("検索", type="primary")

if clicked:
    if len(keyword)  <= 0:
        st.markdown("キーワードは1文字以上でお願いします。")
    else:
        temp_date = date_list[0]
        temp_index_radio = (df_radio["date"].values == temp_date).argmax()
        temp_url = df_radio.loc[temp_index_radio, "url"]
        temp_number = df_radio.loc[temp_index_radio, "number"]

        df_result = myfunc.load_transcripted_dataset(temp_date, create_hms=True)
        df_result["url"] = temp_url
        df_result["number"] = temp_number
        df_result["date"] = temp_date
        df_result = df_result.iloc[0:0].copy()

        for date in date_list:
            df_transcripted = myfunc.load_transcripted_dataset(date, create_hms=True)
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
            df_result["link"] = df_result.apply(lambda df: myfunc.create_youtube_link_html(url, linktext=df["linktext"], time=df["start_s"]), axis=1)

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
