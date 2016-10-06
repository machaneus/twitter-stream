import json
import sys
import matplotlib.pyplot as plt
from states import state_abbreviations,getStateFromLocationString

if __name__ == "__main__":
    state_tweets = dict.fromkeys(state_abbreviations, 0)
    if len(sys.argv) < 2:
        print 'Usage: need to provide tweets filename!'
        exit()
    tweets_file = sys.argv[1]
    with open(tweets_file) as tweets:
        for tweet in tweets.readlines():
            loc = json.loads(tweet)['user']['location']
            state = getStateFromLocationString(loc)
            state_tweets[state]+=1

    plt.bar(range(len(state_tweets)), state_tweets.values(), align='center')
    plt.xticks(range(len(state_tweets)), state_tweets.keys())

    plt.show()



