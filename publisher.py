#!/usr/bin/env python

import tweepy
import MySQLdb
import time
from random import randint
import raven
import re
import logging
import warnings
import numpy as np
import datetime
warnings.filterwarnings('error')
from constants import (EU_TIME_ZONES, EU_LOCATIONS, FOLLOW_INDICATORS, FILTER,
                       FAVOURITE_INDICATORS)
from local_settings import (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME,
                            CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY,
                            ACCESS_SECRET, DB_PREFIX)
from random_walk_bot import *

logger = logging.getLogger(__name__)


def dict_factory(cursor, row):
    """
    Make a dict from a database row.
    """
    return {
        col[0]: row[idx]
        for idx, col in enumerate(cursor.description)
    }


def _tokenised_tweet(tweet_text):
    return re.sub(r'([^\s\w]|_)+', '', tweet_text).lower().split()


def needs_follow(tweet_text):
    return any(v in FOLLOW_INDICATORS for v in _tokenised_tweet(tweet_text))


def needs_fav(tweet_text):
    return any(v in FAVOURITE_INDICATORS for v in _tokenised_tweet(tweet_text))


def fetch_new_tweets_from_db(tz, lc):
    cursor.execute(FILTER) #commented out... no clue what this does
    tweets = cursor.fetchall()
    cursor.execute('SELECT author_id FROM ' + DB_PREFIX + 'follows')
    followers_tuple = cursor.fetchall()
    followers = {follower[0] for follower in followers_tuple}
    prev_author = ""
    prev_tweet_text = ""
    for tweet in tweets:
        error = None
        status = 0

        if needs_follow(tweet[1]) and tweet[3] not in followers:
            # make sure we don't over follow, new limit is 5000
            # https://support.twitter.com/articles/66885?lang=en
            if len(followers_tuple) > 4235:
                cursor.execute(
                    "SELECT author_id FROM " +
                    DB_PREFIX +
                    "follows ORDER BY last_tweet_follow ASC LIMIT 1"
                )
                author_id = cursor.fetchone()[0]
                try:
                    api.destroy_friendship(id=author_id)
                    cursor.execute(
                        "DELETE FROM " +
                        DB_PREFIX + "follows WHERE author_id=%s LIMIT 1",
                        (author_id, )
                    )
                    db.commit()
                except Exception as e:
                    # we may fail to destroy friendship as user was deleted
                    # etc. so we will still continue the process as usual
                    # status = 9
                    error = e
                    logger.error(str(error))
                    client.captureException()

            try:
                api.create_friendship(id=tweet[3], follow=True)
            except Exception as e:
                status = 9
                error = e
                logger.warning(str(error))
                client.captureException()
            else:
                try:
                    cursor.execute(
                        "REPLACE into " + DB_PREFIX +
                        "follows (author_id, last_tweet_follow) VALUES (%s, %s)",
                        (tweet[3], tweet[2].isoformat(" ").encode("ascii"))
                    )
                    db.commit()
                except Exception as e:
                    error = e
                    logger.error(str(error))
                    status = 9

        if needs_fav(tweet[1]):
            try:
                api.create_favorite(id=tweet[0])
            except Exception as e:
                status = 9
                error = e
                logger.warning(str(error))

        if status != 9:
            try:
                if tweet[3] <> prev_author and tweet[1] <> prev_tweet_text:
                    api.retweet(id=tweet[0])
                    status = 1
                    prev_author = tweet[3]
                    prev_tweet_text = tweet[1]
                else:
                    error = "same author as previous or same text as previous"
            except Exception as e:
                status = 9
                error = e
                logger.warning(str(error))
            '''
            else:
                fullTweet = api.get_status(tweet[0])
                if not fullTweet.retweeted:
                    print 'error'
                else:
                    print 'followed'
            '''

        if error is not None:
            try:
                code = error[0][0]['code']
            except (IndexError, KeyError):
                logger.warning(str(error))
            except TypeError:   #added for debugging... "code = error[0][0]['code'] TypeError: string indices must be integers"
                print error
            else:
                if code == 185:
                    time.sleep(60*15)  # we are over our limit, wait 15 minutes
                if code == 161:
                    time.sleep(60*60)  # we are over our limit, wait 60 minutes

        if status != 0:
            cursor.execute(
                "UPDATE " + DB_PREFIX +
                "retweets SET status=%s, error=%s WHERE tweet_id=%s",
                (status, error, tweet[0])
            )
            db.commit()
        else:
            print 'failed to retweet, no error'

        error = None  # avoid leak

        # retweet (tweet) limit is 2400 a day. or 4 actions a minute which
        # average at 35s (Edited to use poisson distribution with lambda of 60)
        time.sleep(np.random.poisson(50))

    if len(tweets) == 0:
        time.sleep(60)
    #added check to make the bot sleep for at least two hours + a random amount of time ~10min
    elif datetime.datetime.now().hour == randint(0,3):
        time.sleep(7200 + np.random.poisson(900))
        api.update_status(get_random_tweet())

if __name__ == '__main__':
    # default to eu
    tz = EU_TIME_ZONES
    lc = EU_LOCATIONS
    logging.basicConfig(
        filename="%sbasic.log" % DB_PREFIX, level=logging.WARNING,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # set Raven
    client = raven.Client(
        dsn='https://de6bc5b15d104a718820935456fe7b81:963ab45cb56f4ae3984f1cc845fc9aec@app.getsentry.com/50508',
        include_paths=['publisher.py']
    )

    # set up tweepy
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    api.update_status(get_random_tweet())
    while True:
        # Set DB connection
        db = MySQLdb.connect(db=DB_NAME,
                             use_unicode=True) #edited from original

        db.row_factory = dict_factory
        cursor = db.cursor()
        fetch_new_tweets_from_db(tz, lc)
        db.close()
        
