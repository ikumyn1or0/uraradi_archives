import csv
import dataclasses
import os


import config as myconfig
import util as myutil


@dataclasses.dataclass()
class Radio:
    date: str
    title: str = dataclasses.field(init=False)
    youtubeid: str = dataclasses.field(init=False)
    length_s: int = dataclasses.field(init=False)
    is_clip: bool = dataclasses.field(init=False)

    def __post_init__(self):
        data_keys = []
        data_items = []
        with open(os.path.join(myconfig.INPUT_PATH, myconfig.PLAYLIST_FILE), encoding="utf-8") as f:
            reader = csv.reader(f)
            columns_name = []
            for index, playlist_row in enumerate(reader):
                if index == 0:
                    columns_name = playlist_row
                    data_keys = playlist_row
                if playlist_row[columns_name.index("date")] == self.date:
                    data_items = playlist_row
                    break
        data_dict = dict(zip(data_keys, data_items))
        self.title = data_dict["title"]
        self.youtubeid = myutil.youtubeurl_to_id(data_dict["url"])
        self.length_s = int(data_dict["length_s"])
        self.is_clip = myutil.is_clip(data_dict["title"])

    def get_title(self, shortened: bool = False) -> str:
        if shortened:
            return myutil.title_to_shortentitle(self.title, self.date)
        else:
            return self.title

    def get_number(self):
        return myutil.title_to_number(self.title, self.date)

    def get_id(self) -> str:
        return self.youtubeid

    def get_guests(self) -> str:
        guests = myutil.title_to_guestlist(self.title, self.date)
        return guests

    def get_length(self) -> int:
        return self.length_s


@dataclasses.dataclass()
class RadioList:
    radios: dict[str, Radio] = dataclasses.field(default_factory=dict, init=False)

    def __post_init__(self):
        dates = myutil.get_radio_dates()
        for date in dates:
            self.radios[date] = Radio(date)

    def get_dates(self):
        return self.radios.keys()

    def get_radio_in(self, date: str) -> Radio:
        if date not in self.radios.keys():
            return None
        else:
            return self.radios[date]

    def get_radios(self):
        return self.radios
