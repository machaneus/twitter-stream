import oauth2 as oauth
import urllib2 as urllib
import twitterkeys as keys
import sys
import json
from states import state_abbreviations

# See assignment1.html instructions or README for how to get these credentials

api_key = keys.api_key
api_secret = keys.api_secret
access_token_key = keys.access_token_key
access_token_secret = keys.access_token_secret

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
class TweetGrabber(object):
    def __init__(self, api_key, api_secret, access_token_key, access_token_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token_key = access_token_key
        self.access_token_secret = access_token_secret

        self.url = "https://stream.twitter.com/1.1/statuses/filter.json"

        self.oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
        self.oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

        self.signature_method = oauth.SignatureMethod_HMAC_SHA1()





    def getTweets(self, term):

        parameters = {'track' : term}

        http_handler  = urllib.HTTPHandler(debuglevel=_debug)
        https_handler = urllib.HTTPSHandler(debuglevel=_debug)
        
        req = oauth.Request.from_consumer_and_token(self.oauth_consumer,
                                             token=self.oauth_token,
                                             http_method="GET",
                                             http_url=self.url, 
                                             parameters=parameters)

        req.sign_request(self.signature_method, self.oauth_consumer, self.oauth_token)

        headers = req.to_header()

        encoded_post_data = None

        opener = urllib.OpenerDirector()
        opener.add_handler(http_handler)
        opener.add_handler(https_handler)

        response = opener.open(req.to_url(), encoded_post_data)

        return response


if __name__ == '__main__':

    assert len(sys.argv)>1
    term = sys.argv[1]
    filename = 'tweets_'+ term + '.txt'
    
    count=0
    twitter_grabber = TweetGrabber(api_key, api_secret, access_token_key, access_token_secret)
    response = twitter_grabber.getTweets(term)
    with open(filename,"w") as tweetsFile:
        for line in response:
            tweet_json = line.strip()
            tweet = json.loads(tweet_json)
            try:
                if tweet['user']['location']:
                    location_words = tweet['user']['location'].replace(',',' ').split(' ')
                    for word in location_words:
                        if word in state_abbreviations:
                            count+=1
                            tweetsFile.write(tweet_json)
                            print "Wrote tweet no. ", count, "location: ", tweet['user']['location']
                            break
            except:
                continue









