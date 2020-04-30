from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
import string
from collections import Counter

# Text preprocessing by removing stopwords & non-ASCII chars, and applies wordnet lemmatizaiton.
# ARGS: txt,a string
# Ouputs: the preprocessed string result
def preprocess_text(txt):
    lemmatizer = WordNetLemmatizer()

    txt = del_non_text(txt)
    word_list = simple_strip(txt)

    # Remove stopwords and lemmatize
    word_list = [word for word in word_list if word not in stopwords.words('english')]
    word_list = [lemmatizer.lemmatize(i) for i in word_list]
    word_list = [word for word in word_list if len(word) > 1]  # remove 1-letter words

    return " ".join(word_list)

# Rudimentary preprocessing by only removing non-ASCII characters.
# ARGS: a string
# outputs: a list of words without \n and punctuation
def simple_strip(txt):
    regex = RegexpTokenizer(r'\w+')

    # Returns only ASCII characters and strips punctuation
    txt = "".join([char for char in txt if char not in string.punctuation and ord(char) < 128])
    word_list = regex.tokenize(txt.lower())  # naive splitting method, virtually equivalent to split()

    return word_list

# Args: string
# Returns: string without URL, tags (@ ...), and random html tags that somehow got into the API
def del_non_text(txt):
    result = []
    for word in txt.split():
        if word.startswith('http'): continue
        elif word.startswith('@'): continue
        elif word.startswith('&amp;'): continue
        elif '&gt' in word: continue
        result.append(word)
    return " ".join(result)

# Args: df, column name which has the preprocessed text, and number of frequent words you want to see
# Returns: A dictionary, sorted descending by most frequent words in all the preprocessed tweets
def get_word_freq(df, column = 'text', items = None):
    tweets = [str(processed_tweet) for processed_tweet in df[column] if str(processed_tweet) != 'nan'] # otherwise causes error if you load file from csv
    all_words = " ".join(tweets).split() # Join all tweets into one string, and then split them into words
    freq = Counter(all_words).most_common(items) # Sort by frequency
    return freq

