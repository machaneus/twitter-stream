import json
from states import state_abbreviations,getStateFromLocationString
from SentimentAnalyzers import AFINNSentimentAnalyzer

class TweetAnalyzer(object):
    def __init__(self, analyzerType = 'AFINN'):
        if analyzerType == 'AFINN':
            self.analyzer = AFINNSentimentAnalyzer('AFINN-111.txt')
        else:
            raise NotImplemented

        self.files = {}

    def loadTweets(self, filename, fileDescriptor):
        f = open(filename)
        tweets = f.readlines()
        f.close()

        self.files[fileDescriptor] = tweets

    def getTweets(self):
        return self.files


    def getTweetNumberByState(self, filename):
        
        tweets_by_state = dict.fromkeys(state_abbreviations,0)

        with open(filename) as tweets:
            for tweet_json in tweets:
                tweet = json.loads(tweet_json)
                tweet_location = tweet['user']['location']

                state = getStateFromLocationString(tweet_location)
                tweets_by_state[state]+=1

        return tweets_by_state

    def getTweetSentimentByState(self, filename):
        
        sentiment_by_state = dict.fromkeys(state_abbreviations,0)

        with open(filename) as tweets:
            for tweet_json in tweets:
                tweet = json.loads(tweet_json)
                tweet_location = tweet['user']['location']
                tweet_text = tweet['text']

                score = self.analyzer.getTextSentiment(tweet_text)

                state = getStateFromLocationString(tweet_location)
                sentiment_by_state[state]+=score

        return sentiment_by_state
