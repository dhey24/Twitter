#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from local_settings import DB_PREFIX

FILTER = "SELECT DISTINCT *  FROM test." + DB_PREFIX + "retweets WHERE tweet_time >= NOW() - INTERVAL 2 DAY ORDER BY tweet_time desc LIMIT 1000"

QUERY = ["retweet win", "rt win", "retweet ticket", "rt ticket", "like for chance" ]

TABLE_PREFIXES = ['tb3']

POSITIVE_KEYWORDS = {"win", "giveaway", "ticket", "tix"}

FOLLOW_INDICATORS = {"follow", "flw", "following"}

FAVOURITE_INDICATORS = {'fav', 'like'}

BANNED_KEYWORDS = ["palette", "makeup","bieber", "belieber","bio", "vote","VOTE", "Vote", "uk"]

IGNORED_USERS = ['732218972918140928', '714498476600639489', '722127946094415872', '742760893730164736', '723857276046589952', '2314748540', '608596665', '4089193038', '578624910', '23097275', '415129347', '3858193100', '1687154144', '427905846', '731201272376926208', '2217730597', '1871974998', '3527608634', '53331157', '3034394356',
'408548387','732218972918140928','2388116544','31145421','1205532768','722127946094415872','224216421','353590158']

IGNORED_KEYWORDS = ['#tsbsbprops', 'xxx', 'baby','€','£','bieber','pokemon', 'tpp', 'vgc09', 'quiz', '_rt_']

# Need to populate with US specific locations - can be found on the tweet object
EU_LOCATIONS = ["charleston, sc", "chicago, il","boston, ma","durham, nc", "chapel hill, nc", "raleigh, nc", "new york, ny", "brooklyn new york", "new york city", "nyc"]

# Need to populate with US specific time zones - can be found on the tweet object
EU_TIME_ZONES = ["eastern time (us & canada)"]
