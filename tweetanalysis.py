import json
import sys
import matplotlib.pyplot as plt
from states import state_abbreviations,getStateFromLocationString

def loadSentimentFile(filename):
    with open(filename) as sentimentFile:
        scores={}
        for line in sentimentFile:
            term, score = line.split("\t")
            scores[term] = int(score)

    return scores

def getTextScore(text, sentiment_scores):
    score = 0
    words = text.split(' ')
    for word in words:
        if word in sentiment_scores:
            score+=sentiment_scores[word]
    return score

if __name__ == "__main__":
    state_tweets = dict.fromkeys(state_abbreviations, 0)
    state_scores = dict.fromkeys(state_abbreviations, 0)

    if len(sys.argv) < 3:
        print 'Usage: need to provide tweets and scores filenames!'
        exit()
    tweets_file = sys.argv[1]
    scores_file = sys.argv[2]
    with open(tweets_file) as tweets:
        for tweet in tweets.readlines():
            loc = json.loads(tweet)['user']['location']
            text = json.loads(tweet)['text']

            state = getStateFromLocationString(loc)
            state_tweets[state]+=1

            score = getTextScore(text, loadSentimentFile(scores_file))
            state_scores[state]+=score

            

    plt.bar(range(len(state_scores)), state_scores.values(), align='center')
    plt.xticks(range(len(state_scores)), state_scores.keys())

    plt.show()



