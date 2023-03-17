import csv
import emoji
import dataclasses
import os


import config as myconfig
import util as myutil


@dataclasses.dataclass()
class Comment:
    timestamp_s: int
    text: str

    def get_text(self, emojized: bool = True):
        if emojized:
            return emoji.emojize(self.text)
        else:
            return self.text


@dataclasses.dataclass()
class Chat:
    date: str
    comments: list[Comment] = dataclasses.field(default_factory=list, init=False)

    def __post_init__(self):
        with open(os.path.join(myconfig.CHAT_PATH, f"{self.date}.csv")) as f:
            reader = csv.reader(f)
            timestamp_s_index = 0
            text_index = 0
            for index, chat_row in enumerate(reader):
                if index == 0:
                    timestamp_s_index = chat_row.index("start_s")
                    text_index = chat_row.index("text")
                else:
                    timestamp_s = int(chat_row[timestamp_s_index])
                    text = chat_row[text_index]
                    self.comments.append(Comment(timestamp_s, text))


@dataclasses.dataclass()
class ChatList:
    chats: dict[str, Chat] = dataclasses.field(default_factory=dict, init=False)

    def __post_init__(self):
        for date in myutil.get_chat_dates():
            self.chats[date] = Chat(date)

    def get_chat_in(self, date: str) -> Chat:
        if date not in self.chats.keys():
            return None
        else:
            return self.chats[date]
