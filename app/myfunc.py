import re
import glob
import pandas as pd

def get_transcripted_csv_list(include_path=False, include_extension=False):
    csv_path_list = glob.glob("./input/*.csv")
    file_list = []
    for csv_path in csv_path_list:
        if "playlist_裏ラジオウルナイト" in csv_path:
            continue
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
def load_radio_dataset(except_clip=False, create_link_html=False, linktext="title", create_bool_transcripted=False):
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
    return df

def load_transcripted_dataset(date, create_hms=False):
    df = pd.read_csv(f"./input/{date}.csv")
    if create_hms:
        df["start_hms"] = df["start_s"].apply(lambda x: str(int(x/3600)).zfill(1)+":"+str(int((x%3600)/60)).zfill(2)+":"+str(x%60).zfill(2))
        df["end_hms"] = df["end_s"].apply(lambda x: str(int(x/3600)).zfill(1)+":"+str(int((x%3600)/60)).zfill(2)+":"+str(x%60).zfill(2))
    return df
