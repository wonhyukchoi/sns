import json
import tweepy
from dataparser import json_parser, data_parser
from plotter import plot_all

"""
Main class that obtains  data from twitter API,
processes the data into json and csv, saves them,
and creates all the analytical images.
"""

if __name__ == "__main__":

	# Fill in the blanks from your twitter API 
	consumer_key = ''
	consumer_secret = ''
	access_key = ''
	access_secret = ''
	user_handle = '' # add an @ before the actual handle 

    # Tweepy initialization
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    cursor = tweepy.Cursor(api.user_timeline, screen_name=user_handle, tweet_mode='extended').items()

    # key: tweet index (integer)
    # value: tweet object as provided by the twitter API
    results = {}
    for n, item in enumerate(cursor):
        results[n] = item._json
        print("Saving item number {}".format(n + 1))

    # The json file holds all raw information.
    with open('data_json.txt', 'w') as outfile:
        json.dump(results, outfile)

    # Convert select attributes from json to csv
    df = json_parser(results)
    df.to_csv('raw_data.csv')

    # Process dataframe, and create all pretty graphs
    df = data_parser(df)
    df.to_csv('data.csv')
    plot_all(df)

