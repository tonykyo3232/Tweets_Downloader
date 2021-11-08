from twitter_client import TwitterClient
from tweet_analyzer import TweetAnalyzer

# disable for now, since this only allows to download 200 tweets as maximum
# def get_twitter_feed():

#     twitter_client = TwitterClient()
#     tweet_analyzer = TweetAnalyzer()

#     api = twitter_client.get_twitter_client_api()

#     x = 'jimcramer'
#     y = 200

#     # twitter api only allows us to download 200 tweets at one time
#     tweets = api.user_timeline(screen_name=x, count=y, tweet_mode='extended')

#     tweet_analyzer.set_account(x)

#     tweet_analyzer.set_num_of_tweets(y)

#     df = tweet_analyzer.tweets_to_data_frame4(tweets)

#     # upload the file to firebase
#     tweet_analyzer.upload_fire_base(df)

def get_twitter_feed(x, y):

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    tweets = twitter_client.get_user_timeline_tweets(x,y)

    tweet_analyzer.set_account(x)

    tweet_analyzer.set_num_of_tweets(y)

    df = tweet_analyzer.tweets_to_data_frame4(tweets)

    # upload the file to firebase
    tweet_analyzer.upload_fire_base(df)

def main():

    get_twitter_feed('jimcramer', 1500)

main()