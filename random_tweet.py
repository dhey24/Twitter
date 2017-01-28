# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 08:04:54 2016

@author: davidhey
"""

import tweepy
import time
from random_walk_bot import *
from local_settings import *

#from secret import *

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

for i in range(5):
    tweet = get_random_tweet()
    print tweet
    api.update_status(tweet)
    time.sleep(60 * 3)