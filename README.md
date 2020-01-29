# twitter_user
### Lightweight, naive analysis of twitter data on one handle.

For one user, this lightweight analysis provides:

* Retweets vs native tweets bar plot
* Tweet time (hour) histogram
* Tweet length histogram
* 3-line timeseries of number of tweets over time, favorites/tweet over time, retweets/tweet over time.
* A csv file with word frequencies.

It also provides:

* A json file with all tweet attributes available in the [twitter API](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object) 
* A csv file with various columns per tweet, such as its post datetime, hashtags, where it quoted/retweeted another tweet, its length, etc. 

Notes: 

* Word frequencies use standard nlp preprocessing procedures, such as stopword removal and non-ASCII removal.
* Currently, only [statuses/user_timeline](https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline) API is supported.