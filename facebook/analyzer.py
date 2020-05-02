from utils import json_files_to_list
from datetime import datetime
from matplotlib import pyplot as plt
from nlp import TextPreprocessor
from utils import MarkdownGenerator


# TODO: add graphing
# TODO: add auto-generate tables in markdown??
class FbMessageAnalyzer:
    def __init__(self):
        self._senders = set()
        self._messages = []
        self._messages_text = []
        self._sender_messages = {}
        self._freq_words = {}
        self._sender_freq_words = {}
        self._time = []

    def load_from_dir(self, path: str, sender='sender_name',
                      content='content', time='timestamp_ms') -> None:
        self._messages = json_files_to_list(path=path)
        self._parse_messages(sender=sender, content=content)
        self._parse_time(time_type=time)
        self._get_freq_words()

    def count_by_person(self) -> dict:
        return {sender: len(messages) for sender, messages
                in self._sender_messages}

    def write_markdown(self, file_name: str):
        md_maker = MarkdownGenerator()
        md_maker.write(file_name=file_name)
        raise NotImplementedError

    def _parse_messages(self, sender='sender_name',
                        content='content') -> None:

        for msg in self._messages:
            if content in msg.keys():
                text = msg[content]
            else:
                text = '<other>'

            self._sender_messages.\
                setdefault(msg[sender], []).append(text)
            self._messages_text.append(text)

        self._senders = set(self._sender_messages.keys())

    def _parse_time(self, time_type='timestamp_ms'):
        if time_type == 'timestamp_ms':
            timestamp_div = 1000
        else:
            raise NotImplementedError

        for msg in self._messages:
            timestamp = msg[time_type] / timestamp_div
            self._time.append(datetime.fromtimestamp(timestamp))

    def _get_freq_words(self):
        text_preprocessor = TextPreprocessor()
        self._freq_words = text_preprocessor.most_freq(
            " ".join(self._messages_text))
        for sender, messages in self._sender_messages.items():
            sender_freq = text_preprocessor.most_freq(" ".join(messages))
            self._sender_freq_words[sender] = sender_freq

    @staticmethod
    def _piechart(data: dict, save_name: str):
        plt.pie(data)
        plt.savefig(save_name)

    @staticmethod
    def _linechart(data: list, save_name: str):
        raise NotImplementedError
