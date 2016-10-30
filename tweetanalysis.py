import json
import sys
import matplotlib.pyplot as plt
from states import state_abbreviations,getStateFromLocationString
from SentimentAnalyzers import AFINNSentimentAnalyzer
from TwitterTools import TweetAnalyzer
import psycopg2

if __name__ == "__main__":
    conn = psycopg2.connect("dbname='twitter_sent_analysis' user='antonis' host='localhost' port='5433' password='123456'")
    cur = conn.cursor()
    
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
    
"""    for key in state_abbreviations.keys():
        cur.execute("UPDATE sentiment SET trump_sent=%d WHERE state='%s'" % (trump_sentiment_state[key],key))
        cur.execute("UPDATE sentiment SET clinton_sent=%d WHERE state='%s'" % (clinton_sentiment_state[key],key))

    conn.commit()"""

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



