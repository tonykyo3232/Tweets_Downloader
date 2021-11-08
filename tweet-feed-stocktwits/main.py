from twitter_client import TwitterClient
from tweet_analyzer import TweetAnalyzer

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

    get_twitter_feed('Stocktwits', 1500)

main()