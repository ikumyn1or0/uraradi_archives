import csv
import datetime
import glob
import os
import re


import config as myconfig


def youtubeurl_to_id(url: str) -> str:
    """
    youtubeのurlからidを抽出
    """
    return re.search(r"v=(\S)+", url).group()[2: 2 + 11]


def youtubeid_to_url(id: str, second: int = None) -> str:
    """
    youtubeの動画idからurlを生成
    seconds引数でタイムスタンプ付きのurlを生成可能
    """
    if second is None:
        return f"https://youtu.be//{id}"
    else:
        return f"https://youtu.be//{id}?t={second}"


def title_to_guestlist_stype01(title: str) -> list[str]:
    """
    ラジオタイトルからゲスト情報を抽出(期間1)
    """
    casts_belong = re.search(r"【\S+ / \S+】$", title).group()
    casts = casts_belong[1: casts_belong.find(" / ")]

    guests = []
    for cast in casts.split("・"):
        if cast != myconfig.HOST_NAME:
            guests.append(cast)
    return guests


def title_to_guestlist_stype02(title: str) -> list[str]:
    """
    ラジオタイトルからゲスト情報を抽出(期間2)
    """
    casts_belong = re.search(r"裏ラジオウルナイト｜.+ // \S+$", title).group()
    casts = casts_belong[10: casts_belong.find(" // ")]

    guests = []
    for cast in casts.split(" / "):
        if cast != myconfig.HOST_NAME:
            guests.append(cast)
    return guests


def title_to_guestlist(title: str, date: str) -> list[str]:
    """
    ラジオタイトルと放送日付からゲスト情報を抽出
    タイトルに記載されていないゲストの情報も追加
    """
    guests = []
    if date <= myconfig.LATEST_DATE_OF_TITLE_STYLE01:
        guests = title_to_guestlist_stype01(title)
    else:
        guests = title_to_guestlist_stype02(title)

    for guestinfo in myconfig.ADDITIONAL_GUESTS_INFO:
        if date == guestinfo["date"]:
            guests.append(guestinfo["guest"])
    return guests


def title_to_number_stype01(title: str) -> list[str]:
    """
    ラジオタイトルからゲスト情報を抽出(期間1)
    """
    if title[0] != "【":
        return title[8:15]
    else:
        return re.search(r"^【\S+】", title).group()[4:-1]


def title_to_number_stype02(title: str) -> list[str]:
    """
    ラジオタイトルからゲスト情報を抽出(期間2)
    """
    return re.search("｜\S+ 裏ラジ", title).group()[1:-4]


def title_to_number(title: str, date: str) -> list[str]:
    """
    ラジオタイトルと放送日付から放送回を抽出
    """
    if "【" in title:
        return title_to_number_stype01(title)
    elif "//" in title:
        return title_to_number_stype02(title)
    else:
        return " "


def title_to_shortentitle_stype01(title: str) -> list[str]:
    """
    ラジオタイトルから短縮タイトルを抽出(期間1)
    """
    if title[0] != "【":
        return title[0: 8]
    else:
        title = title[title.find("】") + 1: title.rfind("【")]
        title = title.rstrip()
        if title[-9:] == "裏ラジオウルナイト":
            title = title[:-9]
            title = title.rstrip()
        if title[-1] == "/":
            title = title[:-1]
        title = title.rstrip()
        return title
        # return title[title.find("】") + 1: title.find("裏ラジオウルナイト") - 1]


def title_to_shortentitle_stype02(title: str) -> list[str]:
    """
    ラジオタイトルから短縮タイトルを抽出(期間2)
    """
    return title[0: title.find("｜")]


def title_to_shortentitle(title: str, date: str) -> list[str]:
    """
    ラジオタイトルと放送日付から放送回を抽出
    """
    if "【" in title:
        return title_to_shortentitle_stype01(title)
    elif "//" in title:
        return title_to_shortentitle_stype02(title)
    else:
        return " "


def seconds_to_hour(seconds: int) -> float:
    """
    秒数表示から時間表示に変換
    """
    return seconds / 3600


def seconds_to_hms(total_seconds: int) -> str:
    """
    秒数表示からhh:mm:ss表示に変換
    """
    abs_total_seconds = abs(total_seconds)
    hours = int(abs_total_seconds / 3600)
    hours_str = str(hours)
    minutes = int((abs_total_seconds - hours * 3600) / 60)
    minutes_str = str(minutes).zfill(2)
    seconds = int(abs_total_seconds % 60)
    seconds_str = str(seconds).zfill(2)
    if total_seconds < 0:
        return f"-{hours_str}:{minutes_str}:{seconds_str}"
    else:
        return f"{hours_str}:{minutes_str}:{seconds_str}"


def seconds_to_time(total_seconds: int) -> datetime.time:
    """
    秒数表示からdatetime.time型に変換
    """
    abs_total_seconds = abs(total_seconds)
    hours = int(abs_total_seconds / 3600)
    if total_seconds < 0:
        hours = -1 * hours
    minutes = int((abs_total_seconds - hours * 3600) / 60)
    seconds = int(abs_total_seconds % 60)
    return datetime.time(hours, minutes, seconds)


def time_to_seconds(time: datetime.time) -> int:
    """
    datetime.time型から秒数に変換
    """
    return time.hour * 3600 + time.minute * 60 + time.second


def to_htmllink(display_text: str, link: str) -> str:
    return f"<a href={link}>{display_text}</a>"


def is_clip(title: str) -> bool:
    return "総集編" in title


def get_radio_dates() -> list[str]:
    date_list = []
    with open(os.path.join(myconfig.INPUT_PATH, myconfig.PLAYLIST_FILE), encoding="utf-8") as f:
        reader = csv.reader(f)
        columns_name = []
        for index, playlist_row in enumerate(reader):
            if index == 0:
                columns_name = playlist_row
            else:
                date = playlist_row[columns_name.index("date")]
                date_list.append(date)
    return date_list


def get_transcript_dates() -> list[str]:
    path_list = glob.glob(os.path.join(myconfig.TRANSCRIPT_PATH, "*.csv"))
    date_list = []
    for path in path_list:
        filename = path.split("\\")[-1]
        date = filename.split(".")[0]
        date_list.append(date)
    return date_list


def get_chat_dates() -> list[str]:
    path_list = glob.glob(os.path.join(myconfig.CHAT_PATH, "*.csv"))
    date_list = []
    for path in path_list:
        filename = path.split("\\")[-1]
        date = filename.split(".")[0]
        date_list.append(date)
    return date_list
