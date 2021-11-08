## Helper module from project [Twitter Data Analysis](https://github.com/tonykyo3232/Tweet_Data_Analysis)
- Download 1500 cleaned tweets from Twitter accounts daily
- [@jimcramer](https://twitter.com/jimcramer?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor)
- [@YahooFinance](https://twitter.com/YahooFinance)
- [@Stocktwits](https://twitter.com/Stocktwits)

### It is currently deplyed in flask app though [HeroKu](heroku.com).

#### In csv file, it includes:
- cleaned version of the tweets
- tweet id
- tweet length
- tweet date
- tweet source
- tweet likes
- num of retweets
- polarity
- sentiment status
- companies

### after download these .csv files, it will be uploaded to [Google Firebase](https://firebase.google.com/)