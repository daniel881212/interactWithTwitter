from tweepy import Cursor
from tweepy import API
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials

# # # # Twitter Client # # # #
class TwitterClient:
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuth().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
            print(tweet)
        return tweets

    def get_friends_list(self, num_friends):
        friends_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friends_list.append(friend)
        return friends_list

    def get_home_timeline(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

# # # # Twitter Authenticator # # # #
class TwitterAuth:

    def authenticate_twitter_app(self):
        authTS = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        authTS.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return authTS

# # # # Twitter Streamer # # # #
class TwitterStreamer:

    def __init__(self):
        self.twitter_authenticator = TwitterAuth()

    def stream_tweets(self, fetched_tweet_filename, hashtag_list):
        # This handles Twitter authentication and the connection to the Twitter streaming API
        listenerTS = TwitterListener(fetched_tweet_filename)
        authTS = self.twitter_authenticator.authenticate_twitter_app()
        streamTS = Stream(authTS, listenerTS)

        # This line filter Twitter Streams to capture data by keywords
        streamTS.filter(track=hashtag_list)



# # # # Twitter Stream Listener # # # #
class TwitterListener(StreamListener):

    def __init__(self, fetched_tweets_filename):
        super().__init__()
        self.fetched_tweets_filename = fetched_tweets_filename


    def on_data(self, raw_data):
        # do things with the data we just streamed
        print(raw_data)
        try:
            with open(self.fetched_tweets_filename, 'w') as tf:
                tf.write(raw_data)
            return True
        except IOError as e:
            print("Error on_data: %s" % str(e))

        return True

    def on_error(self, status_code):
        # do things if there is an error
        if status_code == 420:
            # Returning False on_data method in case rate limit occurs
            return False

        print(status_code)


if __name__ == "__main__":

    hash_tag_list = []
    fetch_tweets_filename = "tweets.json"

    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(fetch_tweets_filename, hash_tag_list)

    twitter_client = TwitterClient('cksc71_yu')
    print(twitter_client.get_user_timeline_tweets(10))