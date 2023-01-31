import copy
import datetime as dt
import glob
import numpy as np
import pandas as pd
import re

CSV_FILE = "playlist_裏ラジオウルナイト.csv"

EXCEPTED_GUEST_INFO = [["2022-10-28", "島村シャルロット"],
                       ["2022-10-28", "宗谷いちか"]]


def extract_videoid_from_youtubeurl(url: str) -> str:
    return re.search(r"v=(\S)+", url).group()[2:].strip()


def seconds_to_hour(total_seconds: int) -> float:
    return total_seconds / 3600


def hours_to_hms(hours: float) -> str:
    if np.isnan(hours):
        return np.NaN
    else:
        return seconds_to_hms(int(hours * 3600))


def time_to_seconds(time: dt.time) -> int:
    return time.hour * 3600 + time.minute * 60 + time.second


def seconds_to_time(total_seconds: int) -> dt.date:
    hours = int(total_seconds / 3600)
    minutes = int((total_seconds - hours * 3600) / 60)
    seconds = total_seconds % 60
    return dt.time(hours, minutes, seconds)


def seconds_to_hms(total_seconds: int) -> str:
    hours = int(total_seconds / 3600)
    minutes = int((total_seconds - hours * 3600) / 60)
    seconds = total_seconds % 60
    return f"{hours}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"


def get_transcript_date() -> list[str]:
    csv_list = glob.glob("./input/transcript/*.csv")
    date_list = []
    for csv in csv_list:
        file = csv.split("/")[-1]
        date = file.split(".")[0]
        date_list.append(date)
    return date_list


def to_html_link(youtube_id: str, text: str, timestamp_s: int = None) -> str:
    if timestamp_s is None:
        return f"<a href=https://youtu.be/{youtube_id}>{text}</a>"
    else:
        return f"<a href=https://youtu.be/{youtube_id}?t={timestamp_s}>{text} {seconds_to_hms(timestamp_s)}</a>"


class Radio:
    def __init__(self, except_clips: bool = False, with_guest_info: bool = False, except_untranscripted_date: bool = False) -> None:
        self.df = self.__initialize_df()
        self.columns = list()
        self.dates = list()
        self.guests = list()
        self.__sync_columns_dates_to_df()
        if except_clips:
            self.__except_clip_from_df()
        if with_guest_info:
            self.__set_guest_info()
        if except_untranscripted_date:
            self.__except_untranscripted_date_from_df()

    def __initialize_df(self) -> pd.DataFrame:
        df = pd.read_csv(f"./input/{CSV_FILE}")
        df["urlid"] = df["url"].apply(extract_videoid_from_youtubeurl)
        df["length_hour"] = df["length_s"].apply(seconds_to_hour)
        df["length_hms"] = df["length_s"].apply(seconds_to_hms)
        return df

    def __sync_columns_dates_to_df(self) -> None:
        self.columns = self.df.columns.to_list()
        self.dates = self.df["date"].unique().tolist()
        if len(self.get_guests()) > 0:
            self.columns = [c for c in self.df.columns.to_list() if c not in self.get_guests()]

    def __except_clip_from_df(self) -> None:
        self.df = self.df[~ self.df["title"].str.contains("総集編")]
        self.df["number"] = self.df["number"].apply(lambda x: x[3:])
        self.df.reset_index(drop=True, inplace=True)
        self.__sync_columns_dates_to_df()

    def __except_untranscripted_date_from_df(self) -> None:
        self.df = self.df[self.df["date"].isin(get_transcript_date())]
        self.df.reset_index(drop=True, inplace=True)
        self.__sync_columns_dates_to_df()

    def __set_guest_info(self) -> None:
        guest_info_list = []
        for _, radio in self.df.iterrows():
            casts_index_start = radio["title"].rfind("【") + 1
            casts_index_end = radio["title"].rfind("/")
            casts = radio["title"][casts_index_start: casts_index_end]
            for cast in casts.split("・"):
                if "大浦るかこ" not in cast:
                    guest_info_row = [radio["date"], cast]
                    guest_info_list.append(guest_info_row)
        for guest_info in EXCEPTED_GUEST_INFO:
            guest_info_list.append(guest_info)
        guest_info_df = pd.DataFrame(guest_info_list, columns=["date", "guest"])
        self.guests = guest_info_df["guest"].unique().tolist()
        onehot_guest_info_df = pd.get_dummies(guest_info_df, columns=["guest"], prefix="", prefix_sep="").groupby(["date"], as_index=False).sum()
        self.df = pd.merge(self.df, onehot_guest_info_df, how="left", on="date")
        self.df[self.get_guests()] = self.df[self.get_guests()].fillna(0)
        self.df[self.get_guests()] = self.df[self.get_guests()].astype(bool)
        self.__sync_columns_dates_to_df()

    def create_html_link_column(self, display_column: str = "title") -> None:
        self.df["link"] = self.df.apply(lambda df: to_html_link(df["urlid"], df[display_column]), axis=1)
        self.__sync_columns_dates_to_df()

    def filter_by_date(self, date):
        self.df = self.df[self.df["date"] == date]
        self.__sync_columns_dates_to_df()

    def get_columns(self) -> list[str]:
        return copy.deepcopy(self.columns)

    def get_guests(self) -> list[str]:
        return copy.deepcopy(self.guests)

    def get_dates(self) -> list[str]:
        return copy.deepcopy(self.dates)

    def get_df(self, columns: list[str] = None, include_guests: bool = False, dates: list[str] = None) -> pd.DataFrame:
        target_columns = []
        if columns is None:
            target_columns.extend(self.get_columns())
        else:
            target_columns.extend([c for c in columns if c in self.get_columns()])
        if include_guests:
            target_columns.extend(self.get_guests())
        target_dates = []
        if dates is None:
            target_dates.extend(self.get_dates())
        else:
            target_dates.extend([d for d in dates if d in self.get_dates()])
        return self.df[target_columns][self.df["date"].isin(target_dates)].reset_index(drop=True)


class Transcript:
    def __init__(self, date) -> None:
        self.date = date
        self.df = self.__initialize_df(date)
        self.columns = list()
        self.__sync_columns_dates_to_df()

    def __initialize_df(self, date, with_guest_info: bool = False) -> pd.DataFrame:
        if date not in get_transcript_date():
            return pd.DataFrame([])
        else:
            df = pd.read_csv(f"./input/transcript/{date}.csv")
            for index in range(len(df) - 1):
                if df.loc[index, "text"] == df.loc[index + 1, "text"]:
                    df.loc[index + 1, "start_s"] = df.loc[index, "start_s"]
            for index in range(len(df) - 1, 0, -1):
                if df.loc[index, "text"] == df.loc[index - 1, "text"]:
                    df.loc[index - 1, "end_s"] = df.loc[index, "end_s"]
            df = df.drop_duplicates()
            df["start_hms"] = df["start_s"].apply(seconds_to_hms)
            df["end_hms"] = df["end_s"].apply(seconds_to_hms)
            radio = Radio(except_clips=False, with_guest_info=with_guest_info)
            radio.filter_by_date(date)
            for column, item in radio.get_df(include_guests=True).items():
                df[column] = item[0]
            return df

    def __sync_columns_dates_to_df(self) -> None:
        self.columns = self.df.columns.to_list()

    def get_columns(self) -> list[str]:
        return copy.deepcopy(self.columns)

    def get_length_s(self) -> int:
        return self.df.loc[1, "length_s"]

    def create_html_link_column(self, display_column: str = None, with_timestamp: bool = True) -> None:
        if display_column is None:
            self.df["link"] = self.df.apply(lambda df: to_html_link(df["urlid"], "", timestamp_s=df["start_s"]), axis=1)
        else:
            self.df["link"] = self.df.apply(lambda df: to_html_link(df["urlid"], df[display_column], timestamp_s=df["start_s"]), axis=1)
        self.__sync_columns_dates_to_df()

    def get_df(self, columns: list[str] = None, keyword: str = None, second_range: tuple[int] = None) -> pd.DataFrame:
        target_columns = []
        if columns is None:
            target_columns.extend(self.get_columns())
        else:
            target_columns.extend([c for c in columns if c in self.get_columns()])
        target_start_s = 0 if second_range is None else second_range[0]
        target_end_s = self.df["end_s"].max() if second_range is None else second_range[1]
        if keyword is None:
            df = copy.deepcopy(self.df)
        else:
            df = copy.deepcopy(self.df[self.df["text"].str.contains(keyword)])
        return df[target_columns][(df["start_s"] >= target_start_s) & (df["end_s"] <= target_end_s)].reset_index(drop=True)
