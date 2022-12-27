import re
import glob
import pandas as pd

def get_transcripted_csv_list(include_path=False, include_extension=False):
    csv_path_list = glob.glob("./input/transcript/*.csv")
    file_list = []
    for csv_path in csv_path_list:
        filename = csv_path
        if not include_path:
            filename = filename.split("/")[-1]
        if not include_extension:
            filename = filename.split(".")[0]
        file_list.append(filename)
    return file_list

def create_youtube_link_html(youtube_url, linktext, time=None):
    # youtubeのurlからリンクを作成
    youtube_link = "https://youtu.be/" + re.search(r"v=(\S)+", youtube_url).group()[2:]
    # 再生時間の追加
    if time is None:
        pass
    else:
        youtube_link = youtube_link + "?t=" + str(time)

    return f'''<a href="{youtube_link}">{linktext}</a>'''

# ラジオの一覧データをpandasで取得する
def load_radio_dataset(except_clip=False, create_link_html=False, linktext="title", create_bool_transcripted=False, create_hour=False, add_guest_info=False):
    # データセットのload
    df = pd.read_csv("./input/playlist_裏ラジオウルナイト.csv")
    # 総集編の除外
    if except_clip:
        df = df[~ df["title"].str.contains("総集編")].reset_index(drop=True)
        df["number"] = df["number"].apply(lambda x: x[3:])
    # html形式のリンクを作成
    if create_link_html:
        df["link"] =df.apply(lambda df: create_youtube_link_html(df["url"], df[linktext], time=None), axis=1)
    if create_bool_transcripted:
        csv_list = get_transcripted_csv_list(include_path=False, include_extension=False)
        df["is_transcripted"] = df["date"].apply(lambda date: date in csv_list)
    if create_hour:
        df["hour"] = (df["length_s"]/3600).round(4)

    if add_guest_info:
        guest_columns = ["date", "guest"]
        guest_list = []
        for _, radio in df.iterrows():
            text = radio["title"][radio["title"].rfind("【")+1:radio["title"].rfind("/")]
            for person in text.split("・"):
                if "大浦るかこ" not in person:
                    row = [radio["date"], person]
                    guest_list.append(row)
            if radio["date"] == "2022-10-28":
                guest_list.append([radio["date"], "島村シャルロット"])
                guest_list.append([radio["date"], "宗谷いちか"])
        guest_df = pd.DataFrame(guest_list, columns=guest_columns)
        df_columns_original = df.columns
        guest_onehot_df = pd.get_dummies(guest_df, columns=["guest"], prefix="", prefix_sep="").groupby(["date"], as_index=False).sum()
        df = pd.merge(df, guest_onehot_df, how="left", on="date")
        df = df.fillna(0)
        for column in df:
            if column not in df_columns_original:
                df[column] = df[column].astype(bool)
        return df, guest_df["guest"].unique().tolist()
    else:
        return df

def load_transcripted_dataset(date, create_hms=False):
    df = pd.read_csv(f"./input/transcript/{date}.csv")
    if create_hms:
        df["start_hms"] = df["start_s"].apply(lambda x: str(int(x/3600)).zfill(1)+":"+str(int((x%3600)/60)).zfill(2)+":"+str(x%60).zfill(2))
        df["end_hms"] = df["end_s"].apply(lambda x: str(int(x/3600)).zfill(1)+":"+str(int((x%3600)/60)).zfill(2)+":"+str(x%60).zfill(2))
    return df

def aggregate_radio_hour_by_date(df_radio, agg_by):
    df = df_radio[["number", "hour", "date"]].copy()
    df["datetime"] = pd.to_datetime(df["date"])
    if agg_by == "W":
        df_result = df.copy()
    else:
        df_result = df.groupby(pd.Grouper(key="datetime", freq=agg_by)).mean(numeric_only=True)
        df_result["date"] = df_result.index.astype(str)
        df_result["number"] = df_result["date"].apply(lambda x: x[2:4]+"年"+x[5:7]+"月から")
        df_result = df_result.reset_index(drop=True)
    df_result = df_result.sort_values(by="date", ascending=False).reset_index(drop=True)
    return df_result[["number", "hour", "date"]]


