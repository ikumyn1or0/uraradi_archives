import re
import glob
import pandas as pd


def get_transcript_list(include_extension: bool = False) -> list:
    """
    書き起こしテキストのファイル名を取得

    Parameters
    ----------
    include_extension : bool
        ファイル名に拡張子を含めるかの指定

    Returns
    -------
    filename_list : list
        書き起こしテキストのファイル名リスト
    """
    transcript_list = glob.glob("./input/transcript/*.csv")
    filename_list = []
    for transcript in transcript_list:
        # パスを削除
        filename = transcript.split("/")[-1]
        # 拡張子を削除
        if not include_extension:
            filename = filename.split(".")[0]
        # リストにファイルを格納
        filename_list.append(filename)

    return filename_list


def create_youtube_html_link(youtube_url: str, link_text: str, time: int = None) -> str:
    """
    yourubeのurlからhtml用のリンクを作成する

    Parameters
    ----------
    youtube_url : str
        youtubeのurl (https://www.youtube.com/watch?v={id})の形式
    link_text : str
        リンクで表示する際のテキスト
    time : int
        再生時刻

    Returns
    -------
    html_link : str
        htmlリンク
    """
    youtube_id = re.search(r"v=(\S)+", youtube_url).group()[2:]
    youtube_link = "https://youtu.be/" + youtube_id
    if time is not None:
        youtube_link = youtube_link + "?t=" + str(time)
    html_link = f'''<a href="{youtube_link}">{link_text}</a>'''

    return html_link


# ラジオの一覧データをpandasで取得する
def get_radio_dataset(except_clip: bool = False) -> pd.DataFrame:
    """
    放送済みラジオの一覧をpandas DataFrame形式で取得

    Parameters
    ----------
    except_clip : bool
        総集編を除外するかを指定

    Returns
    -------
    df : pd.DataFrame
        放送済みラジオの情報
    """
    # ラジオの一覧を取得
    df = pd.read_csv("./input/playlist_裏ラジオウルナイト.csv")

    # 放送時間をhour単位で取得
    df["hour"] = (df["length_s"] / 3600).round(4)

    # 書き起こし済みかを取得
    transcript_list = get_transcript_list(include_extension=False)
    df["is_transcripted"] = df["date"].isin(transcript_list)

    # 総集編の除外
    if except_clip:
        df = df[~ df["title"].str.contains("総集編")]
        df["number"] = df["number"].apply(lambda x: x[3:])
        df = df.reset_index(drop=True)

    # ゲストの情報を追加する
    guest_df_list = []
    for _, radio in df.iterrows():
        date = radio["date"]
        # タイトルから出演者の情報を抜き出す
        casts_str_start_index = radio["title"].rfind("【") + 1
        casts_str_end_index = radio["title"].rfind("/")
        casts = radio["title"][casts_str_start_index:casts_str_end_index]
        for cast in casts.split("・"):
            # ゲストと日付をリストに格納する
            if "大浦るかこ" not in cast:
                row = [date, cast]
                guest_df_list.append(row)
        # 2022-10-28の出演をリストに格納する
        if date == "2022-10-28":
            guest_df_list.append([date, "島村シャルロット"])
            guest_df_list.append([date, "宗谷いちか"])
    # ゲストの情報をDataFrameに変換する
    guest_df_columns = ["date", "guest"]
    guest_df = pd.DataFrame(guest_df_list, columns=guest_df_columns)
    # one-hot表現に変換する
    guest_df_onehot = pd.get_dummies(guest_df, columns=["guest"], prefix="", prefix_sep="").groupby(["date"], as_index=False).sum()
    # ラジオに関するDataFrameとゲストの情報を結合する
    df = pd.merge(df, guest_df_onehot, how="left", on="date")
    df = df.fillna(0)
    # ゲストの一覧を格納
    guest_list = guest_df["guest"].unique().tolist()
    df[guest_list] = df[guest_list].astype(bool)

    return df, guest_list


def get_transcript_dataset(filename: str) -> pd.DataFrame:
    """
    放送済みラジオの一覧をpandas DataFrame形式で取得

    Parameters
    ----------
    filename : str
        書き起こしテキストのファイル名

    Returns
    -------
    df : pd.DataFrame
        書き起こしテキスト
    """
    df = pd.read_csv(f"./input/transcript/{filename}.csv")
    df["start_hms"] = df["start_s"].apply(lambda x: str(int(x / 3600)).zfill(1) + ":" + str(int((x % 3600) / 60)).zfill(2) + ":" + str(x % 60).zfill(2))
    df["end_hms"] = df["end_s"].apply(lambda x: str(int(x / 3600)).zfill(1) + ":" + str(int((x % 3600) / 60)).zfill(2) + ":" + str(x % 60).zfill(2))

    return df


def aggregate_radio_hour_by_date(df_radio, agg_by):
    df = df_radio[["number", "hour", "date"]].copy()
    df["datetime"] = pd.to_datetime(df["date"])
    if agg_by == "W":
        df_result = df.copy()
    else:
        df_result = df.groupby(pd.Grouper(key="datetime", freq=agg_by)).mean(numeric_only=True)
        df_result["date"] = df_result.index.astype(str)
        df_result["number"] = df_result["date"].apply(lambda x: x[2:4] + "年" + x[5:7] + "月から")
        df_result = df_result.reset_index(drop=True)
    df_result = df_result.sort_values(by="date", ascending=False).reset_index(drop=True)
    return df_result[["number", "hour", "date"]]
