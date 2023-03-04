import csv
import dataclasses
import datetime
import glob
import pandas as pd
import re

CSV_FILE = "playlist_裏ラジオウルナイト.csv"

EXCEPTION_GUESTS_INFO = [["2022-10-28", "島村シャルロット"],
                         ["2022-10-28", "宗谷いちか"]]


def from_youtube_url_to_id(url: str) -> str:
    return re.search(r"v=(\S)+", url).group()[2: 2 + 11]


def from_radioinfo_to_guests(date: str, title: str) -> list[str]:
    guests = []
    casts = title[title.rfind("【") + 1: title.rfind("/")]
    for cast in casts.split("・"):
        if "大浦るかこ" not in cast:
            guests.append(cast)
    for info in EXCEPTION_GUESTS_INFO:
        if info[0] == date:
            guests.append(info[1])
    return guests


def from_seconds_to_hour(seconds: int) -> float:
    return seconds / 3600


def from_seconds_to_hms_format(seconds: int) -> str:
    hours = int(seconds / 3600)
    minutes = int((seconds - hours * 3600) / 60)
    seconds = int(seconds % 60)
    return f"{hours}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"


def from_seconds_to_time(seconds: int) -> datetime.time:
    hours = int(seconds / 3600)
    minutes = int((seconds - hours * 3600) / 60)
    seconds = int(seconds % 60)
    return datetime.time(hours, minutes, seconds)


def from_time_to_seconds(time: datetime.time) -> int:
    return time.hour * 3600 + time.minute * 60 + time.second


def get_transcripted_date() -> list[str]:
    csv_list = glob.glob("./input/transcript/*.csv")
    date_list = []
    for path_and_filename in csv_list:
        filename = path_and_filename.split("/")[-1]
        date = filename.split(".")[0]
        date_list.append(date)
    return date_list


def create_html_link(link, text) -> str:
    return f"<a href={link}>{text}</a>"


@dataclasses.dataclass()
class RadioInfo:
    date: str
    title: str = dataclasses.field(default="", init=False, compare=False)
    youtube_id: str = dataclasses.field(default="", init=False, compare=False)
    length_s: int = dataclasses.field(default=0, init=False, compare=False)
    guests: list[str] = dataclasses.field(default_factory=list, init=False, compare=False)
    is_transcripted: bool = dataclasses.field(default=True, init=False, compare=False)
    is_clip: bool = dataclasses.field(default=False, init=False, compare=False)

    def __post_init__(self):
        csv_columns = []
        with open(f"./input/{CSV_FILE}") as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 0:
                    csv_columns = row
                elif row[csv_columns.index("date")] == self.date:
                    self.title = row[csv_columns.index("title")]
                    self.youtube_id = from_youtube_url_to_id(row[csv_columns.index("url")])
                    self.length_s = int(row[csv_columns.index("length_s")])
                    break
        self.guests = from_radioinfo_to_guests(self.date, self.title)
        self.is_transcripted = self.date in get_transcripted_date()
        self.is_clip = "総集編" in self.title

    def get_length_hour(self):
        return self.length_s / 3600

    def get_length_hms(self):
        return from_seconds_to_hms_format(self.length_s)

    def get_youtube_url(self, second: int = None) -> str:
        url = f"https://youtu.be//{self.youtube_id}"
        if second is not None:
            url = url + f"?t={second}"
        return url

    def get_shorten_title(self):
        shorten_title = ""
        if "#74" in self.title:
            shorten_title = "#74"
        elif self.is_clip:
            shorten_title = self.title[5:15]
        else:
            shorten_title = self.title[4:7]
        return shorten_title


@dataclasses.dataclass()
class RadioList:
    dates: list[str] = dataclasses.field(default_factory=list, init=False)
    RadioInfos: list[RadioInfo] = dataclasses.field(default_factory=list, init=False)

    def __post_init__(self):
        self.dates = pd.read_csv(f"./input/{CSV_FILE}")["date"].tolist()
        for date in self.dates:
            self.RadioInfos.append(RadioInfo(date))

    def get_guest_list(self):
        guests = []
        for radioinfo in self.RadioInfos:
            guests.extend(radioinfo.guests)
        return list(set(guests))

    def get_radioinfo_in(self, date):
        if date not in self.dates:
            return None
        else:
            for radioinfo in self.RadioInfos:
                if date == radioinfo.date:
                    break
            return radioinfo


@dataclasses.dataclass(frozen=True)
class Text:
    start_s: int
    end_s: int
    text: str


@dataclasses.dataclass()
class Transcript:
    date: str
    texts: list[Text] = dataclasses.field(default_factory=list, init=False)

    def __post_init__(self):
        csv_columns = []
        with open(f"./input/transcript/{self.date}.csv") as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 0:
                    csv_columns = row
                else:
                    start_s = int(row[csv_columns.index("start_s")])
                    end_s = int(row[csv_columns.index("end_s")])
                    text = row[csv_columns.index("text")]
                    self.texts.append(Text(start_s, end_s, text))


@dataclasses.dataclass()
class TranscriptList:
    dates: list[str] = dataclasses.field(default_factory=list, init=False)
    Transcripts: list[Transcript] = dataclasses.field(default_factory=list, init=False)

    def __post_init__(self):
        self.dates = get_transcripted_date()
        for date in self.dates:
            self.Transcripts.append(Transcript(date))

    def get_transcript_in(self, date):
        if date not in self.dates:
            return None
        else:
            for transcript in self.Transcripts:
                if date == transcript.date:
                    break
            return transcript
