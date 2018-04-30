
import json
import os
import pandas as pd
import tweepy
from tweepy import OAuthHandler
from datetime import datetime
import jsonpickle
import re
import matplotlib.pyplot as plt


#### functions ####
def date_strip(tweetdate):
    ''' Function that converts JSON tweet date format to y/mm/dd format'''
    # Use re to get rid of the milliseconds.
    remove_ms = lambda x:re.sub("\+\d+\s","", x)
    
    # Make the string into a datetime object.
    mk_dt = lambda x:datetime.strptime(remove_ms(x), "%a %b %d %H:%M:%S %Y")
    
    # Format your datetime object.
    my_form = lambda x:"{:%Y-%m-%d}".format(mk_dt(x))
    
    return my_form(tweetdate)


#### USING TWEEPY #### 


#keys 
access_token = ''
access_secret = ''
consumer_key = ''
consumer_secret = ''

#set auth
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
   
#create twitter API wrapper 
api = tweepy.API(auth)

#Switching to application authentication
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
#Setting up new api wrapper, using authentication only
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
 

query = 'lang:en "boycott starbucks" OR #boycottstarbucks OR starbucks'
#query = 'lang:en #boycott OR boycott'

#Maximum number of tweets to collect
maxTweets = 10000

#Open a JSON file to save the tweets to
tweetCount = 0
with open('boycott_tweets_sbux.json', 'w') as f:

    
    for tweet in tweepy.Cursor(api.search,q=query, until='2018-04-29').items(maxTweets) :         

                  
        #Write the JSON format to the text file
        f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
        tweetCount += 1

    #Display tweets collected
    print("Downloaded {0} tweets".format(tweetCount))


filename = 'boycott_tweets_sbux.json'

tweets = [] 
with open(filename, 'r') as f: 
    for line in f.readlines(): 
        tweets.append(json.loads(line))

#create select dataframe 
df = pd.DataFrame()

df['text'] = list(map(lambda tweet: tweet['text'], tweets))
df['timestamp'] = list(map(lambda tweet: tweet['created_at'], tweets))
df['date'] = df['timestamp'].apply(lambda x:date_strip(x))
df.head()


df.groupby('date').text.count().plot()
plt.title("U.S. Daily 'Boycott Starbucks' Tweets")
plt.ylabel('number of tweets')
plt.ylim(0, 80)

plt.savefig('sbux_tweets_by_day.png')


#### USING PYTHON TWITTER TOOLS (PTT) LIBRARY ##### 

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

## STREAM TWEETS 


# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)

# Get a sample of the public data following through Twitter
iterator = twitter_stream.statuses.sample()

# Print each tweet in the stream to the screen 
# Here we set it to stop after getting 10 tweets. 
tweet_count = 10
for tweet in iterator:
    tweet_count -= 1
    # Twitter Python Tool wraps the data returned by Twitter 
    # as a TwitterDictResponse object.
    # We convert it back to the JSON format to print/score
    print( json.dumps(tweet) ) 
    
    # The command below will do pretty printing for JSON data, try it out
    # print json.dumps(tweet, indent=4)
       
    if tweet_count <= 0:
        break 

tweet_count = 10
with open('boycott_tweets.json', 'w') as f:

    for tweet in iterator:

           #Write the JSON format to the text file
            f.write(json.dumps(tweet) + '\n')
            tweet_count -= 1
            
            if tweet_count <= 0:
                break

#import tweets data 
df = pd.read_json('boycott_tweets.json', lines=True, orient='columns') #creates a pandas dataframe         
df.head()           


## SEARCH TWITTER API 
#set up API 
t = Twitter(auth=oauth)
res = t.search.tweets(q="#pycon")

                      
                      
####### USING PYTHON-TWITTER PACKAGE ##### 


#Setting up Twitter API (using python-twitter package)
api = twitter.Api(
 consumer_key = CONSUMER_KEY ,
 consumer_secret = CONSUMER_SECRET,
 access_token_key = ACCESS_TOKEN,
 access_token_secret = ACCESS_SECRET
 )








