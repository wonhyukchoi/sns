from string import punctuation
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
from wrappers import timer


class TextPreprocessor:
    def __init__(self, lang='eng'):
        self._lang = lang.strip().lower()
        if self._lang != 'eng':
            raise NotImplementedError

    @timer
    def preprocess(self, text: str, ascii_only=True, rm_stopword=True):
        if ascii_only:
            text = "".join(char for char in text if ord(char) < 128)

        text = "".join(char for char in text if char not in punctuation)

        if rm_stopword:
            if self._lang != 'eng':
                raise NotImplementedError

            word_list = text.split()
            text = " ".join(word for word in word_list
                            if word not in stopwords.words('english'))

        return text

    @staticmethod
    @timer
    def lemmatize(text: str, min_word_len=2):
        lemmatizer = WordNetLemmatizer()
        word_list = text.split()
        lemmatized = tuple(lemmatizer.lemmatize(word) for word in word_list)
        pruned_text = " ".join(word for word in lemmatized
                               if len(word) >= min_word_len)
        return pruned_text

    @timer
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
