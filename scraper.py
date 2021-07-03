import tweepy
from tweepy import OAuthHandler
import datetime
import preprocessor as p
import re
from textblob import TextBlob

consumer_key=''
consumer_secret=''
access_key=''
access_secret=''


def auth():
    try:
        auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
        auth.set_access_token(access_key,access_secret)
        api= tweepy.API(auth)
    except:
        print("AN error occured during authentication")
    return api


def get_tweets(api,date_until,words):
    tweets=tweepy.Cursor(api.search,q=words,until=date_until,
                wait_on_rate_limit=True, tweet_mode='extened').items(50)
    list_tweets=[[tweet.text] for tweet in tweets]
    print(list_tweets)

    return list_tweets

api=auth()

#get trending words from backend 
#check trendings words from previous batch

words='#ArrestThugRamdev'
date_until=datetime.date.today()

data=get_tweets(api,date_until,words)
# get_tweets(api,date_until,"#PMSales")

#1st time preprocessing
def preprocess(data):
    res=''
    for d in data:
        # text=p.clean(d[0])
        text=' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|([RT])', ' ', d[0].lower()).split())
        res =''.join(text)
        print(text)
    return res
print("                         #######################                     ")

after_data=preprocess(data)

print(after_data)

#preprocess 2nd time

# def secend_pre(data):
#     tweet=''
#     for d in data:
#         text=re.sub(r'https?:\/\/\S+','',d)
#         text=re.sub(r'\[\[(?:[^\]|]*\|)?([^\]|]*)\]\]', r'\1', d)
#         tweet.append(text)
#     return tweet

def sentiment(data):
    res=TextBlob(data)
    print(res.sentiment.polarity)
    if res.sentiment.polarity <0:
        return 'Negative'
    elif res.sentiment.polarity ==0:
        return 'Netual'
    else:
        return 'positive'

final_res=sentiment(after_data)
print(final_res)
