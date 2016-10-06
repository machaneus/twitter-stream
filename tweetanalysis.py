import json
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print 'Usage: need to provide tweets filename!'
        exit()
    tweets_file = sys.argv[1]
    with open(tweets_file) as tweets:
        for tweet in tweets.readlines():
            print json.loads(tweet)['user']['location'], '\t\t', json.loads(tweet)['text']


