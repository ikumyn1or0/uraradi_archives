import os

HOST_NAME = "大浦るかこ"

INPUT_PATH = os.path.join(".", "input")
CHAT_PATH = os.path.join(INPUT_PATH, "chat")
TRANSCRIPT_PATH = os.path.join(INPUT_PATH, "transcript")

PLAYLIST_FILE = "playlist_裏ラジオウルナイト.csv"

ADDITIONAL_GUESTS_INFO = [{"date": "2022-10-28",
                           "guest": "島村シャルロット"},
                          {"date": "2022-10-28",
                           "guest": "宗谷いちか"}
                          ]

LATEST_DATE_OF_TITLE_STYLE01 = "2023-02-28"

PAGE_TITLE = "裏ラジアーカイブス"
PAGE_ICON = "🦉"
SITE_TITLE = "📻裏ラジアーカイブス🦉"

TEXT_DATA_SELECTOR = {"書き起こしのみ": 0,
                      "チャットのみ": 1,
                      "両方": 2}
