import csv
import dataclasses
import os


import config as myconfig
import util as myutil


@dataclasses.dataclass()
class TranscriptText:
    start_s: int
    end_s: int
    text: str


@dataclasses.dataclass()
class Transcript:
    date: str
    texts: list[TranscriptText] = dataclasses.field(default_factory=list, init=False)

    def __post_init__(self):
        with open(os.path.join(myconfig.TRANSCRIPT_PATH, f"{self.date}.csv"), encoding="utf-8") as f:
            reader = csv.reader(f)
            start_s_index = 0
            end_s_index = 0
            text_index = 0
            for index, transcript_row in enumerate(reader):
                if index == 0:
                    start_s_index = transcript_row.index("start_s")
                    end_s_index = transcript_row.index("end_s")
                    text_index = transcript_row.index("text")
                else:
                    start_s = int(transcript_row[start_s_index])
                    end_s = int(transcript_row[end_s_index])
                    text = transcript_row[text_index]
                    self.texts.append(TranscriptText(start_s, end_s, text))

    def get_texts(self):
        return self.texts


@dataclasses.dataclass()
class TranscriptList:
    transcripts: dict[str, Transcript] = dataclasses.field(default_factory=dict, init=False)

    def __post_init__(self):
        for date in myutil.get_transcript_dates():
            self.transcripts[date] = Transcript(date)

    def get_transcript_in(self, date: str) -> Transcript:
        if date not in self.transcripts.keys():
            return None
        else:
            return self.transcripts[date]