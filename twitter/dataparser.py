import pandas as pd
from nlp import preprocess_text, del_non_text
from tqdm import tqdm
"""
Converts data obtained from tweepy into a dataframe.
Also creates useful columns, such as tweet hour, post length, preprocessed text, etc. 
"""


# ARGS: list/dict of json
# Returns: dataframe
# Hardcoded for tweepy. Converts json format to dataframe.
# assumes each tweet info is a dictionary's keys, and the values are indices which are discarded.
def json_parser(data):
    df = pd.DataFrame()

    for status in data.values():
        datetime = status['created_at']
        raw_text = status['full_text']
        retweeted = raw_text.startswith('RT')
        hashtags = status['entities']['hashtags']
        quoted = status['is_quote_status']
        retweet_count = status['retweet_count']
        favorite_count = status['favorite_count']
        result = {'time': datetime, 'raw_text': raw_text, 'retweeted': retweeted, 'hashtags': hashtags,
                  'quoted': quoted, 'retweet_count' : retweet_count, 'favorite_count': favorite_count}
        df = df.append(result, ignore_index= True)

    return df

# Args: dataframe
# Returns: dataframe with two new columns:
# 1) date of tweet (w/o time)
# 2) hour of tweet (twitter handle's timezone.)
def date_parser(df, column = 'datetime'):
    df['datetime'] = pd.to_datetime(df[column])
    # TODO: inefficient duplication
    df['date'] = pd.to_datetime(df['datetime'].apply(lambda x: x.date()))
    df['time'] = df['datetime'].apply(lambda x: x.hour)
    return df

# Args: dataframe
# Returns: dataframe with two new columns:
# 1) preprocesed text (note nlp file)
# 2) length of original post, w/o tags and link
def text_parser(df, column = 'raw_text'):
    df['text'] = [preprocess_text(item) for item in tqdm(df[column])]
    df['post_len'] = [len(del_non_text(item)) for item in df[column]]
    return df

# Args: dataframe
# Returns: dataframe with columns created by date_parser and text_parser.
def data_parser(df, text_column = 'raw_text', datetime_column = 'datetime'):
    df = date_parser(df, datetime_column)
    df = text_parser(df, text_column)
    return df

if __name__ == "__main__":
    df = pd.read_csv('raw_data.csv')
    data_parser(df).to_csv('data.csv')
