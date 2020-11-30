
from uuid import uuid4
from datetime import datetime
import tweepy

class Twitter_Scraper(object):

    def __init__(self
                 , consumer_key
                 , consumer_secret
                 , access_token
                 , access_token_secret
                 , output_locn):
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._access_token = access_token
        self._access_token_secret = access_token_secret

        self._output_locn = output_locn

    def get_tweets(self):

        auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
        auth.set_access_token(self._access_token, self._access_token_secret)
        api = tweepy.API(auth)

        #only goes 7 days in the past - without preimum
        tweets = tweepy.Cursor(api.search
                               , q = 'covid19'
                               , lang = 'en'
                               , since = '2020-11-29'
##                               , until = '2020-11-29'
                               , result_type = 'mixed'
                               , tweet_mode = 'extended'
                               ).items(200)
        for i in tweets:
            date = i.created_at.strftime('%Y%m%d%H%M%S')
            f_id = str(uuid4())
            filename = self._output_locn + '\\' + date + '__' + f_id + '.txt'
            with open(filename, 'w', encoding = 'utf-8') as f:
                f.write(i.full_text)

def main():
    #vars...
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_token_secret = ''

    output_locn = r''

    #run...
    scraper = Twitter_Scraper(consumer_key, consumer_secret
                              , access_token, access_token_secret
                              , output_locn)

    scraper.get_tweets()

if __name__ == '__main__':
    main()
