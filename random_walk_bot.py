# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 21:03:48 2016

@author: davidhey
"""

#lukebot.py
import pickle,random
import pprint
a=open('lexicon_allmytweets','rb')
successorlist=pickle.load(a)
keys = []
for k, v in successorlist.iteritems():
    keys.append(k)
a.close()
def nextword(a):
    if a in successorlist and len(successorlist[a]) > 0:
        return random.choice(successorlist[a])
    else:
        return 'the'

def get_random_tweet():
    tLen = 141
    while tLen > 140:
        Len = 0
        while Len == 0:    
            speech=random.choice(keys)
            Len = len(successorlist[speech])
            #print Len
        #print(speech)
        s=random.choice(speech.split())
        response=''
        while True:
            neword=nextword(s)
            response+=' '+neword
            s=neword
            if neword[-1] in '?!.':            
                break
        twt = speech[:1].upper() + speech[1:] + response
        tLen = len(twt)
    return twt

pprint.pprint(get_random_tweet())

        
