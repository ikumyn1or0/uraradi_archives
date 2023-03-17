import pandas as pd


import config as myconfig
import setting as mysetting
import util as myutil


def get_df_of_date_titlelink():
    radiolist = mysetting.load_RadioList()
    columns = ["date", "titlelink"]
    table = []
    for date in radiolist.get_dates():
        radio = radiolist.get_radio_in(date)
        title = radio.get_title()
        link = myutil.youtubeid_to_url(radio.get_id())
        row = [date, myutil.to_htmllink(title, link)]
        table.append(row)
    df = pd.DataFrame(table, columns=columns)
    return df


def get_dict_of_date_title():
    result_dict = {}
    radiolist = mysetting.load_RadioList()
    for date, radio in radiolist.get_radios().items():
        text = radio.get_number() + "：" + radio.get_title(shortened=True)
        result_dict[text] = date
    return result_dict


def able_to_plot_textdata(date, text_type):
    if text_type in [0, 2]:
        if date not in myutil.get_transcript_dates():
            return False
    if text_type in [1, 2]:
        if date not in myutil.get_chat_dates():
            return False
    return True


def limit_dataframe_rows(dataframe, rows_num):
    return dataframe.head(rows_num)


def get_df_of_timestamplink_text(date, text_style, range_s):
    radiolist = mysetting.load_RadioList()
    radio = radiolist.get_radio_in(date)

    columns = ["text_type", "timestamplink", "text"]
    for_sort_columns = ["seconds", "texttype", "text_temp"]
    for_sort_ascending = [True, True, True]
    table = []
    if text_style in [0, 2]:
        transcriptlist = mysetting.load_TranscriptList()
        transcript = transcriptlist.get_transcript_in(date)
        for transcripttext in transcript.texts:
            if (range_s[0] <= transcripttext.start_s) & (transcripttext.end_s <= range_s[1]):
                display_text = myutil.seconds_to_hms(transcripttext.start_s)
                link = myutil.youtubeid_to_url(radio.get_id(), transcripttext.start_s)
                row = [myconfig.TRANSCRIPT_TYPE_EMOJI,
                       myutil.to_htmllink(display_text, link),
                       transcripttext.text,
                       transcripttext.start_s,
                       0,
                       transcripttext.text]
                table.append(row)
    if text_style in [1, 2]:
        chatlist = mysetting.load_ChatList()
        chat = chatlist.get_chat_in(date)
        for comment in chat.comments:
            if (range_s[0] <= comment.timestamp_s) & (comment.timestamp_s <= range_s[1]):
                display_text = myutil.seconds_to_hms(comment.timestamp_s)
                link = myutil.youtubeid_to_url(radio.get_id(), comment.timestamp_s)
                text = comment.get_text(emojized=True)
                row = [myconfig.CHAT_TYPE_EMOJI,
                       myutil.to_htmllink(display_text, link),
                       text,
                       comment.timestamp_s,
                       1,
                       comment.text]
                table.append(row)
    df = pd.DataFrame(table, columns=columns + for_sort_columns)
    df = df.sort_values(by=for_sort_columns, ascending=for_sort_ascending)
    df = df[columns]
    return df
