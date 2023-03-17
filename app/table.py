import datetime
import streamlit as st


import config as myconfig
import preprocess as mypreprocess
import setting as mysetting
import util as myutil


def plot_radio():
    columns_dict = {"date": "放送日付",
                    "titlelink": "タイトル"}
    date_col_name = columns_dict["date"]
    df = mypreprocess.get_df_of_date_titlelink()
    df = df[columns_dict.keys()]
    df = df.rename(columns=columns_dict)
    df = df.sort_values(by=date_col_name, ascending=False).reset_index(drop=True)
    st.write(df.to_html(escape=False,
                        index=False,
                        col_space={date_col_name: "110px"},
                        justify="center"),
             unsafe_allow_html=True,)


def sloder_for_length_filter(date: str, disabled: bool = False):
    radiolist = mysetting.load_RadioList()
    radio = radiolist.get_radio_in(date)

    min_value_default = datetime.time(hour=0, minute=0, second=0)
    max_value_default = myutil.seconds_to_time(radio.get_length())
    min_value = datetime.time(hour=0, minute=0, second=0)
    max_value = myutil.seconds_to_time(radio.get_length())
    target_range = st.slider("表示する再生時間を絞り込んでください。",
                             value=(min_value_default, max_value_default),
                             min_value=min_value, max_value=max_value,
                             step=datetime.timedelta(minutes=1),
                             format="H:mm:ss",
                             disabled=disabled)
    return [myutil.time_to_seconds(target_range[0]),
            myutil.time_to_seconds(target_range[1])]


def plot_transcript_chat():
    columns_dict = {"text_type": " ", "timestamplink": "再生時間",
                    "text": "テキスト"}
    timestamp_col_name = columns_dict["timestamplink"]

    title_date_selector = mypreprocess.get_dict_of_date_title()
    target_title = st.selectbox(label="表示する放送回を選択してください。", options=title_date_selector.keys())
    target_date = title_date_selector[target_title]

    target_text_key = st.radio(label="表示するデータを選択してください。", options=myconfig.TEXT_DATA_SELECTOR.keys())
    target_text_style = myconfig.TEXT_DATA_SELECTOR[target_text_key]

    flag_plottable = mypreprocess.able_to_plot_textdata(target_date, target_text_style)

    target_range = sloder_for_length_filter(target_date, disabled=not flag_plottable)

    if flag_plottable:
        df = mypreprocess.get_df_of_timestamplink_text(target_date, target_text_style, target_range)
        df = df[columns_dict.keys()]
        df = df.rename(columns=columns_dict)
        if len(df) > myconfig.MAX_ROWS:
            st.markdown(f"表示する件数を全{len(df)}件中{myconfig.MAX_ROWS}件に制限しています。")
        else:
            st.markdown(f"全{len(df)}件を表示しています。")
        df = mypreprocess.limit_dataframe_rows(df, myconfig.MAX_ROWS)
        df = df.reset_index(drop=True)
        st.write(df.to_html(escape=False,
                            index=False,
                            col_space={timestamp_col_name: '110px'},
                            justify="center"),
                 unsafe_allow_html=True)
    else:
        st.markdown("データの追加までお待ちください。")
