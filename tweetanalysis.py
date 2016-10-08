import json
import sys
import matplotlib.pyplot as plt
from states import state_abbreviations,getStateFromLocationString

class AFINNSentimentAnalyzer(object):

    def __init__(self, filename):
        self.scores = self.loadSentimentFile(filename)
   
    def loadSentimentFile(self, filename):
        with open(filename) as sentimentFile:
            scores={}
            for line in sentimentFile:
                term, score = line.split("\t")
                scores[term] = int(score)

        return scores

    def getTextSentiment(self,text):
        score = 0
        words = text.split(' ')
        for word in words:
            if word in self.scores:
                score+=self.scores[word]
        return score

class TweetAnalyzer(object):
    def __init__(self, analyzerType = 'AFINN'):
        if analyzerType == 'AFINN':
            self.analyzer = AFINNSentimentAnalyzer('AFINN-111.txt')
        else:
            raise NotImplemented

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





if __name__ == "__main__":
    state_tweets = dict.fromkeys(state_abbreviations, 0)
    state_scores = dict.fromkeys(state_abbreviations, 0)


    if len(sys.argv) < 3:
        print 'Usage: need to provide tweets and scores filenames!'
        exit()
    tweets_file = sys.argv[1]
    scores_file = sys.argv[2]

    analyzer = AFINNSentimentAnalyzer(scores_file)
    tweetAnalyzer = TweetAnalyzer()
    state_tweets = tweetAnalyzer.getTweetSentimentByState(tweets_file)
    
    '''with open(tweets_file) as tweets:
        for tweet in tweets.readlines():
            loc = json.loads(tweet)['user']['location']
            text = json.loads(tweet)['text']

            state = getStateFromLocationString(loc)
            state_tweets[state]+=1

            score = analyzer.getTextSentiment(text)
            state_scores[state]+=score'''


            

    plt.bar(range(len(state_tweets)), state_tweets.values(), align='center')
    plt.xticks(range(len(state_tweets)), state_tweets.keys())

    plt.show()



