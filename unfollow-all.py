import MySQLdb
import tweepy
import sqlite3
import time
import re

from local_settings import (CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY,
                            ACCESS_SECRET)

if __name__ == '__main__':
    auth = tweepy.auth.OAuthHandler(
        consumer_key='x93UbCbAVV28QRwdXLg2qwJoj',
        consumer_secret='YxnegBGEjX5C35UyPaIbHultGSMuL1i3ZzGL7zkPqDxWR39dHr')
    auth.set_access_token(
        '804184616-IUqMtRcW6RrlWXtLhGV6l4YKDFNqOliO1A9xLy5G',
        'dYiZGy5MJM9AekXNLbuZOcOejB1ndSluxVVBvBc6nP2FF')

    api = tweepy.API(auth_handler=auth)

    for friend in tweepy.Cursor(api.friends).items():
        friend.unfollow()
        print friend.screen_name
        time.sleep(5)
