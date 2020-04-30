import nltk
from nltk.corpus import stopwords


class Preprocessor:
    def remove_punkt(self, text=''):
        raise NotImplementedError

    def lemmatize(self, text=''):
        raise NotImplementedError
