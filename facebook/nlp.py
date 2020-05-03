import re
from nltk import corpus
from nltk.stem import WordNetLemmatizer
from collections import Counter


class TextPreprocessor:
    def __init__(self, lang='eng', stopwords=None):
        self._lang = lang.strip().lower()
        if self._lang != 'eng':
            raise NotImplementedError

        self._stopwords = stopwords

    def preprocess(self, text: str, ascii_only=True, rm_stopword=True):
        if ascii_only:
            text = self._ascii_only(text)

        if rm_stopword:
            text = self._rm_stopword(text)

        return text

    @staticmethod
    def lemmatize(text: str, min_word_len=2):
        lemmatizer = WordNetLemmatizer()
        word_list = text.split()
        lemmatized = tuple(lemmatizer.lemmatize(word) for word in word_list)
        pruned_text = " ".join(word for word in lemmatized
                               if len(word) >= min_word_len)
        return pruned_text

    def most_freq(self, text: str, preprocess=True, lemmatize=True, max_num=None,
                  ascii_only=True, rm_stopword=True, min_word_len=2):

        if preprocess:
            text = self.preprocess(text, ascii_only=ascii_only,
                                   rm_stopword=rm_stopword)
        if lemmatize:
            text = self.lemmatize(text, min_word_len=min_word_len)

        word_list = text.split()
        freq_words = Counter(word_list).most_common(max_num)
        return freq_words

    @staticmethod
    def _ascii_only(text: str):
        text = re.sub(r'[^a-zA-Z ]', '', text)
        text = re.sub(r'\s\s+', ' ', text)
        return text

    def _rm_stopword(self, text: str):
        """
        This may take a while.
        :param text: Any string to strip
        :return:
        """
        if self._lang != 'eng':
            raise NotImplementedError
        else:
            stopwords = corpus.stopwords.words('english')

        if self._stopwords:
            stopwords += self._stopwords

        word_list = [word.lower() for word in text.split()]

        text = " ".join(word for word in word_list
                        if word not in stopwords)

        return text
