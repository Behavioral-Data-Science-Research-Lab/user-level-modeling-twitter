#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
FUNCTION: The purpose of this script is to scrape Twitter for Tweets containing
          text from the lists below pertaining to online learning before 
          and after COVID-19

LAST UPDATED: 08/26/2021

OWNER: David J. Cox
'''

try:
    import snscrape.modules.twitter as sntwitter
except:
    pip3 install git+https://github.com/JustAnotherArchivist/snscrape.git
    import snscrape.modules.twitter as sntwitter
    
import pandas as pd

# Personal preference
pd.set_option('display.max_columns', None)

#%% Get all of my tweets
!snscrape twitter-user davidjcox_ > my_tweets.json

# Read in the json file
tweets = pd.read_json('my_tweets.json', lines=True)

# Convert to dataframe
tweets = pd.DataFrame(tweets)

#%%
# Creating list to append tweet data 
tweets_list1 = []

# Using TwitterSearchScraper to scrape data and append tweets to list
for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:davidjcox_').get_items()): #declare a username 
    tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.user.username]) #declare the attributes to be returned
    
# Creating a dataframe from the tweets list above 
tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

#%% Scrape Twitter for seed dataframe
!snscrape --jsonl --progress --max-results 10000000 --since 2020-03-01 twitter-search "#digitallearning until:2020-05-01" > text-query-tweets.json

# Read in the json file
online_tweets = pd.read_json('text-query-tweets.json', lines=True)

# Creating a dataframe from the tweets list above
online_tweets = pd.DataFrame(online_tweets)

#%% All online learning words

for i in online_learning:
    !snscrape --jsonl --progress --max-results 10000000 --since 2020-03-01 twitter-search "$i until:2020-05-01" > text-query-tweets.json

    # Read in the json file
    add_tweets = pd.read_json('text-query-tweets.json', lines=True)

    # Creating a dataframe from the tweets list above
    add_tweets = pd.DataFrame(add_tweets)

    # Add new data to our growing list
    online_tweets = online_tweets.append(add_tweets)

#%% Add col and save it
online_tweets['time'] = 'pre-COVID'
online_tweets.to_csv('pre_covid_learning.csv')

#%% Scrape Twitter for seed dataframe
!snscrape --jsonl --progress --max-results 10000000 --since 2021-03-01 twitter-search "digital learning until:2021-05-01" > text-query-tweets.json

# Read in the json file
online_tweets_post = pd.read_json('text-query-tweets.json', lines=True)

# Creating a dataframe from the tweets list above
online_tweets_post = pd.DataFrame(online_tweets_post)

#%%
for i in online_learning:
    !snscrape --jsonl --progress --max-results 10000000 --since 2021-03-01 twitter-search "$i until:2021-05-01" > text-query-tweets.json

    # Read in the json file
    add_tweets = pd.read_json('text-query-tweets.json', lines=True)

    # Creating a dataframe from the tweets list above
    add_tweets = pd.DataFrame(add_tweets)

    # Add new data to our growing list
    online_tweets_post = online_tweets_post.append(add_tweets)

#%% Add col and save it
online_tweets_post['time'] = 'post-COVID'
online_tweets_post.to_csv('post_covid_learning.csv')

#%% Concatenate all the dfs to each other
print("Expected length: ", len(online_tweets) + len(online_tweets_post))
all_tweets = online_tweets.append(online_tweets_post)
print("Observed length: ", len(all_tweets))

#%% Save it
all_tweets.to_csv('higher_ed_twitter_scrape.csv')

#%% Freeze requirements.txt
!pip3 freeze > requirements.txt
