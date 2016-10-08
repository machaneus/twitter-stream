import json
import sys
import matplotlib.pyplot as plt
from states import state_abbreviations,getStateFromLocationString
from SentimentAnalyzers import AFINNSentimentAnalyzer
from TwitterTools import TweetAnalyzer


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


    clinton_sentiment_state = tweetAnalyzer.getTweetSentimentByState('tweets_clinton_1000.txt')
    trump_sentiment_state = tweetAnalyzer.getTweetSentimentByState('tweets_trump_1000.txt')

    tr_cl = dict([(key, trump_sentiment_state[key]-clinton_sentiment_state[key]) for key in trump_sentiment_state.keys()])

    plt.bar(range(len(clinton_sentiment_state)), clinton_sentiment_state.values(), align='center')
    plt.xticks(range(len(clinton_sentiment_state)), clinton_sentiment_state.keys())

    plt.show()

    plt.bar(range(len(trump_sentiment_state)), trump_sentiment_state.values(), align='center')
    plt.xticks(range(len(trump_sentiment_state)), trump_sentiment_state.keys())


    plt.show()

    plt.bar(range(len(tr_cl)), tr_cl.values(), align='center')
    plt.xticks(range(len(tr_cl)), tr_cl.keys())


    plt.show()



