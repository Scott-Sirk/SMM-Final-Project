
from collections import defaultdict
from uuid import uuid4
from datetime import datetime
import pandas as pd
import tweepy
import re

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

        d = defaultdict(list)

        auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
        auth.set_access_token(self._access_token, self._access_token_secret)
        api = tweepy.API(auth)

        indiana = '39.795002,-86.160226,120km'
        illinois = '39.805289,-89.458871,160km'
        texas = '32.144136,-99.192757,450km'
        new_mexico = '34.530234,-105.916390,260km'


        #only goes 7 days in the past - without preimum
        tweets = tweepy.Cursor(api.search
                               , q = 'covid19'
                               , geo = new_mexico
                               , lang = 'en'                               
                               , result_type = 'mixed'
                               , tweet_mode = 'extended'
                               ).items(1000)
        for i in tweets:
            date = i.created_at.strftime('%Y%m%d%H%M%S')
            f_id = str(uuid4())

            d['id'].append(str(uuid4()))
            d['create_date'].append(str(i.created_at))
            d['state'].append('new_mexico')
            d['sentiment'].append('UNKNOWN')
            d['text'].append(re.sub('[\s]+', ' ', i.full_text.replace(',', ' ')))

        df = pd.DataFrame(d)
        df.to_csv(self._output_locn, index = False)
            

def main():
    #vars...
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_token_secret = ''

    output_locn = r'data/states/new_mexico.csv'

    #run...
    scraper = Twitter_Scraper(consumer_key, consumer_secret
                              , access_token, access_token_secret
                              , output_locn)

    scraper.get_tweets()

if __name__ == '__main__':
    main()
