from matplotlib import pyplot as plt
from matplotlib import dates
import pandas as pd
import numpy as np
from nlp import get_word_freq
"""
Creates useful twitter user analysis pictures,
such as # of retweets to native tweets, time of tweet, length of tweet, etc.
Except for retweet_ratio, all analyses discount retweets and only analyze native tweets.
"""


# Args: df
# Returns: barplot of # of retweets v.s. # of native tweets
def retweet_ratio(df, column = 'retweeted'):
    total = len(df)
    retweeted = len(df[df[column] == 1]) # number of retweets
    plt.bar('tweets posted', total-retweeted)
    plt.bar('retweets posted', retweeted)
    plt.title('Native tweets posted v.s. retweets posted')
    plt.ylabel('Tweets')
    plt.savefig('retweet_count.png')
    plt.clf()

# Args: df
# Returns: histogram of user tweet hour
def tweet_time(df, column = 'time'):
    df = df[df['retweeted'] == 0]
    plt.hist(df[column])
    plt.title('Tweets by time')
    plt.xlabel('Hour')
    plt.ylabel('Tweets')
    plt.savefig('tweet_time.png')
    plt.clf()

# Args: df
# Returns: 3-line plot of number of retweets, favorites, tweet count per month
def tweet_reacts(df, column='datetime'):

    df['datetime'] = pd.to_datetime(df[column]) # converts datetime into correct type
    df = df[df['retweeted'] == 0].sort_values(by='datetime', ascending=True) # removes retweets
    df['month'] = df['datetime'].apply(lambda x: str(x.year) + "/" + str(x.month)) # creates "month" column

    # Get dates for plotting
    df['matplotdate'] = dates.date2num(pd.to_datetime(df['month']))

    df['dummy'] = [1] * len(df)  # dummy variable for pivot table frequency count
    pivot = pd.pivot_table(df, index='month', aggfunc=np.sum) # sum metrics of each day into their respective months

    # Code to format dates nicely on matplotlib.
    # Currently using year since months clog up too much space.
    # TODO: parametrize to user year, month, or day depending on developer choice.
    ax = plt.gca()
    ax.xaxis.set_major_locator(dates.YearLocator())
    ax.xaxis.set_major_formatter(dates.DateFormatter('%Y'))
    month = list(set(df['matplotdate'])) # x-axis
    month.sort()

    plt.plot(month, pivot['dummy'], label='Total tweets')
    plt.plot(month, pivot['favorite_count'] / pivot['dummy'], label='Favorites per tweet')
    plt.plot(month, pivot['retweet_count'] / pivot['dummy'], label='Retweets per tweet')
    plt.legend()

    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.title('Tweet metrics over time')
    plt.savefig('timeseries.png')
    plt.clf()

# Args: df
# Returns: histogram of tweet lengths
def post_len_hist(df, column='post_len'):
    df = df[df['retweeted'] == 0]
    plt.hist(df[column])
    plt.title('Length of tweets')
    plt.xlabel('Characters')
    plt.ylabel('Number of tweets')
    plt.savefig('tweet_len.png')
    plt.clf()

# Args: df
# Returns: csv of words by frequency, after preprocessing (note nlp.py)
def output_freq_words(df, column = 'text', items = None):
    df = df[df['retweeted'] == 0]
    freq = get_word_freq(df, column, items)
    pd.DataFrame(freq, columns=['word', 'frequency']).to_csv('word_freq.csv')

# Args: runs all analysis code
# TODO: proper parameterization
def plot_all(df):
    retweet_ratio(df)
    tweet_time(df)
    tweet_reacts(df)
    post_len_hist(df)
    output_freq_words(df)

if __name__ == "__main__":
    df = pd.read_csv('data.csv')
    plot_all(df)

