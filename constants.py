#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
#from local_settings import DB_PREFIX


QUERY = ["retweet win", "rt win", ]

TABLE_PREFIXES = ['tb1']

POSITIVE_KEYWORDS = {"win", "giveaway"}

FOLLOW_INDICATORS = {"follow", "flw"}

FAVOURITE_INDICATORS = {'fav', 'like'}

BANNED_KEYWORDS = ["vote"]

IGNORED_USERS = []

IGNORED_KEYWORDS = ['pokemon', 'tpp', 'vgc09', 'quiz', '_rt_',]

# Need to populate with US specific locations - can be found on the tweet object
EU_LOCATIONS = ["New York, NY", 'Brooklyn New York', 'New York City', 'NYC']

# Need to populate with US specific time zones - can be found on the tweet object
EU_TIME_ZONES = ["Eastern Time (US & Canada)"]
