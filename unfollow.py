# Unfollow oldest 100 follwers from DB

import MySQLdb
import tweepy
import sqlite3
import time
import re

from local_settings import (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME,
                            CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY,
                            ACCESS_SECRET, DB_PREFIX)

# Set DB connection
db = MySQLdb.connect(host=DB_HOST,
                     user=DB_USER,
                     passwd=DB_PASSWORD,
                     db=DB_NAME,
                     use_unicode=True)

if __name__ == '__main__':
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    cursor = db.cursor()
    cursor.execute('SELECT * FROM ' + DB_PREFIX + 'follows ORDER BY last_tweet_follow LIMIT 300')
    followers = cursor.fetchall()
    for follower in followers:
        try:
            api.destroy_friendship(id=follower[0])
            cursor.execute("DELETE FROM " + DB_PREFIX + "follows WHERE author_id='%s' LIMIT 1" % (follower[0]))
            db.commit()
            print follower[1], follower[0]
        except Exception as e:
            print e
        time.sleep(3)
