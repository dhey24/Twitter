#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
#import MySQLdb
import json
from datetime import datetime
import sys
import re
import raven

from constants import (IGNORED_KEYWORDS, IGNORED_USERS, QUERY,
                       EU_LOCATIONS, EU_TIME_ZONES, TABLE_PREFIXES)
from local_settings import (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME,
                            CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY,
                            ACCESS_SECRET)#, STACK, DB_PREFIX)

## Set DB connection
#db = MySQLdb.connect(host=DB_HOST,
#                     user=DB_USER,
#                     passwd=DB_PASSWORD,
#                     db=DB_NAME,
#                     use_unicode=True,)
#
#db.set_character_set('utf8mb4')
#cursor = db.cursor()
#cursor.execute("SET NAMES utf8mb4")
#cursor.execute("SET CHARACTER SET utf8mb4")
#cursor.execute("SET character_set_connection=utf8mb4")
retweets_to_populate = []


# Basic Matching for new tweets:
# 1. original tweet has more than 10 retweets
# 2. original tweet author isn't in our banned user list
# 3. Author does not use default avatar
# 4. Author has more than 100 followers
def is_good_tweet(tweet_dict):
    if tweet_dict['user']['id'] in IGNORED_USERS:
        return False
    if tweet_dict['retweet_count'] < 10:
        return False

    if tweet_dict['user']['default_profile_image'] is True:
        return False

    if tweet_dict['user']['followers_count'] < 100:
        return False

    return True


def no_ignored_keywords(tweet_dict):
    text = tweet_dict['text']
    clean_text = re.sub(r'([^\s\w]|_)+', '', text).lower()
    tweet_text_dict = [word for word in clean_text.split(" ")]
    if any(map(lambda v: v in clean_text, IGNORED_KEYWORDS)):
        return False
    return True


def not_too_old(tweet_dict):
    tweet_date = datetime.strptime(tweet_dict['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    now = datetime.now()
    if (now - tweet_date).days > 7:
        return False

    return True


def good_location(decoded):
    time_zone = decoded['user']['time_zone']
    if time_zone is None or time_zone.lower() not in EU_TIME_ZONES:
            return False

    location = decoded['user']['location']
    if location is None or location.lower() not in EU_LOCATIONS:
        return False

    return True


def good_url(decoded):
    url = decoded['user']['url']
    if url is None or '.uk' in url or 'uk.' in url:
        return True

    return False


def good_text_indicators(decoded):
    tweet_text = decoded['text'].encode('utf-8')
    if '€' in tweet_text or '£' in tweet_text or 'worldwide' in tweet_text:
        return True

    return False


def get_tweet_obj(decoded):
    if 'retweeted_status' in decoded:
        if 'quoted_status' in decoded['retweeted_status']:
            return decoded['retweeted_status']['quoted_status']

        return decoded['retweeted_status']


# This is the listener, responsible for receiving data
class StdOutListener(tweepy.StreamListener):

    def on_data(self, data):

        global retweets_to_populate
        decoded = json.loads(data)
        tweet_obj = get_tweet_obj(decoded)

        if tweet_obj and is_good_tweet(tweet_obj) and no_ignored_keywords(tweet_obj) and not_too_old(tweet_obj):
            if good_location(tweet_obj) or good_url(tweet_obj) or good_text_indicators(tweet_obj):
                tweet_text = tweet_obj['text'].encode('utf-8')
                time_zone = tweet_obj['user']['time_zone']
                if time_zone is not None:
                    time_zone.encode('utf-8')
                location = tweet_obj['user']['location']
                if location is not None:
                    location.encode('utf-8')
                retweets_to_populate.append((
                    tweet_obj['id'],
                    tweet_text,
                    datetime.strptime(tweet_obj['created_at'], '%a %b %d %H:%M:%S +0000 %Y'),
                    tweet_obj['user']['id'],
                    0,
                    time_zone,
                    location,
                    's-poller',
                    tweet_obj['user']['url']
                ))
            if len(retweets_to_populate) > 10:
#                for prefix in TABLE_PREFIXES:
#                    cursor.executemany('INSERT IGNORE INTO ' + prefix + '_retweets(tweet_id, tweet_text, tweet_time, author_id, time_zone, location, url, status, poller) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)', retweets_to_populate)
#                    db.commit()
#                retweets_to_populate = []
                print "oops this got commented out"

    def on_error(self, status_code):
        client.captureMessage('Encountered error with status code:' + repr(status_code.encode('utf-8')))
        return True

    def on_disconnect(self, notice):
        client.captureMessage('disconnected from twitter:' + repr(notice.encode('utf-8')))
        return True

    def on_timeout(self):
        print 'Timeout...'
        client.captureMessage('connection timeout')
        return True

if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

    # set Raven
    client = raven.Client(
        dsn='https://de6bc5b15d104a718820935456fe7b81:963ab45cb56f4ae3984f1cc845fc9aec@app.getsentry.com/50508',
        include_paths=['consumer.py']
    )

    stream = tweepy.Stream(auth, l)
    stream.filter(track=QUERY)
#    db.close()
