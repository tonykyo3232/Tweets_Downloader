"""
Provides functionalities for analyzing and categorizing content from tweets.
"""
from io import StringIO
from io import BytesIO
from textblob import TextBlob

import numpy as np
import pandas as pd               # to be able to store data in data frame
import re                         # regular expression
import datetime
import os
import pyrebase

import company_list
import popular_twitter_accounts


class TweetAnalyzer():

    '''
    default constructor
    '''
    def __init__(self):
        self._date = str(datetime.date.today())
        self._directory = "default"
        self._tweet_account = ""
        self._num_of_tweets = 0

    # getter method
    def get_account(self):
        return self._tweet_account
    
    def get_num_of_tweets(self):
        return self._num_of_tweets

    def get_directory(self):
        return self._directory

    # setter method
    def set_account(self, x):
        self._tweet_account = x

    def set_num_of_tweets(self, x):
        self._num_of_tweets = x

    # get twitter user name
    def get_user_name(self, val):
        for key, value in popular_twitter_accounts.accounts.items():
            if val == value:
                return key
        return "key doesn't exist"

    # return the file name with its tweet account and number of tweets 
    def get_filename(self):
        return self._date + "_@" + self._tweet_account + "_" + str(self._num_of_tweets) + "_tweets"

    """
    Use regular expression library to clear the text
    - removing special characters from tweets
    - remove hyper links
    """
    def clean_tweet(self, tweet):
        cleaned_text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

        # Debug
        # print("Original text:")
        # print("------------")
        # print(tweet)
        # print("------------\n")

        # print("Cleaned text:")
        # print("------------")
        # print(cleaned_text)
        # print("============\n\n")

        return cleaned_text


    '''
    save the tweets to data frame of: tweet, id, len, date, source, likes, retweets
    '''
    def tweets_to_data_frame4(self, tweets):

        # extract the texts from each of those tweets
        df = pd.DataFrame(data=[self.clean_tweet(tweet.full_text) for tweet in tweets], columns=['tweets'])

        # id
        df['id'] = np.array([tweet.id for tweet in tweets]) 
        
        # length
        df['len'] = np.array([len(tweet.full_text) for tweet in tweets])
       
        # date
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        
        # source
        df['source'] = np.array([tweet.source for tweet in tweets])
        
        # number of likes
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        
        # number of retweet
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        result = self.sentiment_tweet(df)

        #
        df['polarity'] = pd.DataFrame(result[0], columns=['polarity'])

        #
        df['sentiment'] = pd.DataFrame(result[1], columns=['sentiment'])

        #
        df['companies'] = pd.DataFrame(result[2], columns=['companies'])

        return df

    '''
    save the tweets to data frame of: tweet, date, source, likes, retweets
    '''
    def tweets_to_data_frame3(self, tweets):

        # extract the texts from each of those tweets
        df = pd.DataFrame(data=[self.clean_tweet(tweet.full_text) for tweet in tweets], columns=['tweets'])

        return df

    '''
    save the tweets to data frame of: tweet, date, source, likes, retweets
    '''
    def tweets_to_data_frame2(self, tweets):

        # extract the texts from each of those tweets
        df = pd.DataFrame(data=[self.clean_tweet(tweet.full_text) for tweet in tweets], columns=['tweets'])

        # date
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        
        # source
        df['source'] = np.array([tweet.source for tweet in tweets])
        
        # number of likes
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        
        # number of retweet
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df

    '''
    save the tweets to data frame of: tweet, id, len, date, source, likes, retweets
    '''
    def tweets_to_data_frame(self, tweets):

        # extract the texts from each of those tweets
        df = pd.DataFrame(data=[tweet.full_text for tweet in tweets], columns=['tweets'])

        # id
        df['id'] = np.array([tweet.id for tweet in tweets]) 
        
        # length
        df['len'] = np.array([len(tweet.full_text) for tweet in tweets])
       
        # date
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        
        # source
        df['source'] = np.array([tweet.source for tweet in tweets])
        
        # number of likes
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        
        # number of retweet
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df


    '''
    extract the hashtag from tweets
    '''
    def hashtag_extract(self, tweets):
        hashtags = []
        # loop words in the tweet
        for tweet in tweets:
            ht = re.findall(r"#(\w+)", tweet)
            if(len(ht)):
                hashtags.append(ht)
        return hashtags


    '''
    check if tweets contains any company's name from the dictionary fron company_list.py
    '''
    def detect_companies(self, df):
        
        company_names = company_list.companies.keys()
        tweets = df['tweets']

        # create an empty dictionary
        # result = {}
        result = [] # temp

        # iterating through tweets
        for tweet in tweets:
            
            # print(tweet)
            #split each tweet into a list of words
            words = tweet.split()

            for word in words:
                if word in company_names:
                    print("found key word: [" + word + "]")
                    result.append(word)

        if len(result) == 0:
            print("no companies found from tweets")
        else:    
            print("=======================")
            print(result)
            print("=======================")


    '''
    save the tweets in .csv file
    '''
    def save_as_csv(self, df, num_of_tweets):
        df.to_csv((self.get_filename() + '.csv'), index=False)


    '''
    get the tweets in .csv file
    '''
    def get_csv(self, df):
        return df.to_csv(None, index=False)

    # https://www.programcreek.com/python/example/120344/pandas.compat.BytesIO
    def upload_fire_base(self, df):

        # please enter your own cofig data
        config = {
          "apiKey": "",
          "authDomain": "",
          "projectId": "",
          "storageBucket": "",
          "messagingSenderId": "",
          "appId": "",
          "measurementId": "",
          "databaseURL": ""
        }

        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()

        buf = BytesIO()
        str_buf = StringIO()

        df.to_csv(str_buf, index=False)

        buf = BytesIO(str_buf.getvalue().encode('utf-8'))

        file = buf

        path_on_cloud = self.get_account() + "/downloaded_tweets/" + self.get_filename() + ".csv"
        path_local = file
        storage.child(path_on_cloud).put(path_local)

    '''
    doing the sentiment analysis of the tweets. It will categorized the tweets into group of positive, netural and negative
    '''
    def sentiment_tweet(self, df):
        
        tweets = df['tweets']

        sentiment_list = []
        polarity_list = []
        company_list = []

        # iterating through tweets fetched
        for tweet in tweets:

            # clean the junk message
            analysis = TextBlob(self.clean_tweet(tweet))

            companies = self.detect_companies(tweet)

            # neutral
            if (analysis.sentiment.polarity == 0):
                polarity_list.append(analysis.sentiment.polarity)
                sentiment_list.append('neutral')
            # wpositive
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                polarity_list.append(analysis.sentiment.polarity)
                sentiment_list.append('wpositive')
            # positive
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                polarity_list.append(analysis.sentiment.polarity)
                sentiment_list.append('positive')
            # spositive
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                polarity_list.append(analysis.sentiment.polarity)
                sentiment_list.append('spositive')
            # wnegative
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                polarity_list.append(analysis.sentiment.polarity)
                sentiment_list.append('wnegative')
            # negative
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                polarity_list.append(analysis.sentiment.polarity)
                sentiment_list.append('negative')
            # snegative
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                polarity_list.append(analysis.sentiment.polarity)
                sentiment_list.append('snegative')

            company_list.append(companies)

        return (polarity_list, sentiment_list, company_list)


    '''
    check if tweets contains any company's name from the dictionary fron company_list.py
    '''
    def detect_companies(self, tweet):
        
        company_names = company_list.companies.keys()

        # create an empty dictionary
        result = ''

        #split each tweet into a list of words
        words = tweet.split()

        for word in words:
            if word in company_names:
                if(word not in result):
                    # print("found key word: [" + word + "]")
                    curr = word + ", "
                    result = result + curr


        if(len(result) == 0):
            result += 'None'
        else:
            result = result[:-2] # remove ',' at the end

        return result