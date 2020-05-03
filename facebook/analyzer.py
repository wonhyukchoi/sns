from utils import json_files_to_list
from datetime import datetime
from matplotlib import pyplot as plt
from nlp import TextPreprocessor
from utils import MarkdownGenerator


# TODO: add graphing
# TODO: add auto-generate tables in markdown??
class FbMessageAnalyzer:
    def __init__(self, lang='eng', stopwords=None):
        self._senders = set()
        self._messages = []
        self._messages_text = []
        self._sender_messages = {}
        self._freq_words = {}
        self._sender_freq_words = {}
        self._time = []

        lang = lang.lower().strip()
        if lang == 'english':
            lang = 'eng'
        self._lang = lang
        self._stopwords = stopwords

    def load_json_in_dir(self, path: str):
        self._messages = json_files_to_list(path=path)

    def parse_data(self, sender='sender_name',
                   content='content', time='timestamp_ms',
                   preprocess=True, lemmatize=True,
                   max_num=None, ascii_only=True,
                   rm_stopword=True, min_word_len=2) -> None:
        self._parse_messages(sender=sender, content=content)
        self._parse_time(time_type=time)
        self._get_freq_words(preprocess=preprocess, lemmatize=lemmatize,
                             max_num=max_num, ascii_only=ascii_only,
                             rm_stopword=rm_stopword,
                             min_word_len=min_word_len)

    def make_graphs(self,time_series='time_series',
                    sender_ratio='message_ratio'):
        raise NotImplementedError

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

            self._sender_messages. \
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

    # FIXME: refactor
    def _get_freq_words(self, preprocess=True, lemmatize=True,
                        max_num=None, ascii_only=True, rm_stopword=True,
                        min_word_len=2):
        text_preprocessor = TextPreprocessor(lang=self._lang,
                                             stopwords=self._stopwords)

        self._freq_words = text_preprocessor.most_freq(
            " ".join(self._messages_text),
            preprocess=preprocess, lemmatize=lemmatize, max_num=max_num,
            ascii_only=ascii_only, rm_stopword=rm_stopword,
            min_word_len=min_word_len)

        for sender, messages in self._sender_messages.items():
            sender_freq = text_preprocessor.most_freq(
                " ".join(messages),
                preprocess=preprocess, lemmatize=lemmatize, max_num=max_num,
                ascii_only=ascii_only, rm_stopword=rm_stopword,
                min_word_len=min_word_len)

            self._sender_freq_words[sender] = sender_freq

    @staticmethod
    def _piechart(data: dict, save_name: str):
        plt.pie(data)
        plt.savefig(save_name)

    @staticmethod
    def _linechart(data: list, save_name: str):
        raise NotImplementedError
